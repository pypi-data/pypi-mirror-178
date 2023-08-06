import json
from pathlib import Path
from typing import Optional, List, Union, Tuple, Dict

import requests
import torch
import torch.nn as nn
import random
import tempfile
import os

from huggingface_hub import hf_hub_download
from torch.nn import CrossEntropyLoss

from transformers.utils import (
add_start_docstrings_to_model_forward,
add_end_docstrings,
replace_return_docstrings,
)

from transformers import AutoModelForSeq2SeqLM
from transformers.models.bart.modeling_bart import (
    BartForConditionalGeneration,
    _expand_mask, logger,
    shift_tokens_right,
    BART_INPUTS_DOCSTRING,
    _CONFIG_FOR_DOC,
    BART_GENERATION_EXAMPLE,
    BartModel,
    BartDecoder

)
from .adapter import Adapter
from transformers.modeling_outputs import (
    BaseModelOutputWithPastAndCrossAttentions,
    Seq2SeqModelOutput,
    BaseModelOutput,
    Seq2SeqLMOutput
)

from huggingface_hub.utils import validate_hf_hub_args,HfFolder
from huggingface_hub.hf_api import HfApi
from huggingface_hub.repository import Repository
from huggingface_hub.constants import CONFIG_NAME, PYTORCH_WEIGHTS_NAME


class KeyBartAdapter(BartForConditionalGeneration):
    def __init__(self,adapter_hid_dim:int) -> None:
        keyBart = AutoModelForSeq2SeqLM.from_pretrained("bloomberg/KeyBART")
        self.__fix_weights__(keyBart)

        super().__init__(keyBart.model.config)
        # super().__init__()

        self.lm_head = keyBart.lm_head
        self.model = BartPlus(keyBart, adapter_hid_dim)
        self.register_buffer("final_logits_bias", torch.zeros((1, self.model.shared.num_embeddings)))
        self.config = keyBart.config



    def __fix_weights__(self,keyBart:BartForConditionalGeneration):
        for i in keyBart.model.parameters():
            i.requires_grad = False
        for i in keyBart.lm_head.parameters():
            i.requires_grad = False

    def save_pretrained(
        self,
        save_directory: Union[str, Path],
        config: Optional[dict] = None,
        push_to_hub: bool = False,
        **kwargs,
    ):
        """
        Save weights in local directory.

        Parameters:
            save_directory (`str` or `Path`):
                Specify directory in which you want to save weights.
            config (`dict`, *optional*):
                Specify config (must be dict) in case you want to save
                it.
            push_to_hub (`bool`, *optional*, defaults to `False`):
                Whether or not to push your model to the Hugging Face Hub after
                saving it. You can specify the repository you want to push to with
                `repo_id` (will default to the name of `save_directory` in your
                namespace).
            kwargs:
                Additional key word arguments passed along to the
                [`~utils.PushToHubMixin.push_to_hub`] method.
        """
        os.makedirs(save_directory, exist_ok=True)

        # saving model weights/files
        self._save_pretrained(save_directory)

        # saving config
        if isinstance(config, dict):
            path = os.path.join(save_directory, CONFIG_NAME)
            with open(path, "w") as f:
                json.dump(config, f)

        if push_to_hub:
            kwargs = kwargs.copy()  # soft-copy to avoid mutating input
            if config is not None:  # kwarg for `push_to_hub`
                kwargs["config"] = config

            if (
                # If a deprecated argument is passed, we have to use the deprecated
                # version of `push_to_hub`.
                # TODO: remove this possibility in v0.12
                kwargs.get("repo_url") is not None
                or kwargs.get("repo_path_or_name") is not None
                or kwargs.get("organization") is not None
                or kwargs.get("git_user") is not None
                or kwargs.get("git_email") is not None
                or kwargs.get("skip_lfs_files") is not None
            ):
                if kwargs.get("repo_path_or_name") is None:
                    # Repo name defaults to `save_directory` name
                    kwargs["repo_path_or_name"] = save_directory
            elif kwargs.get("repo_id") is None:
                # Repo name defaults to `save_directory` name
                kwargs["repo_id"] = Path(save_directory).name

            return self.push_to_hub(**kwargs)

    @classmethod
    @validate_hf_hub_args
    def from_pretrained(
            cls,
            pretrained_model_name_or_path: str,
            force_download: bool = False,
            resume_download: bool = False,
            proxies: Optional[Dict] = None,
            token: Optional[Union[str, bool]] = None,
            cache_dir: Optional[str] = None,
            local_files_only: bool = False,
            revision: Optional[str] = None,
            **model_kwargs,
    ):
        r"""
        Download and instantiate a model from the Hugging Face Hub.

                Parameters:
                    pretrained_model_name_or_path (`str` or `os.PathLike`):
                        Can be either:
                            - A string, the `model id` of a pretrained model
                              hosted inside a model repo on huggingface.co.
                              Valid model ids can be located at the root-level,
                              like `bert-base-uncased`, or namespaced under a
                              user or organization name, like
                              `dbmdz/bert-base-german-cased`.
                            - You can add `revision` by appending `@` at the end
                              of model_id simply like this:
                              `dbmdz/bert-base-german-cased@main` Revision is
                              the specific model version to use. It can be a
                              branch name, a tag name, or a commit id, since we
                              use a git-based system for storing models and
                              other artifacts on huggingface.co, so `revision`
                              can be any identifier allowed by git.
                            - A path to a `directory` containing model weights
                              saved using
                              [`~transformers.PreTrainedModel.save_pretrained`],
                              e.g., `./my_model_directory/`.
                            - `None` if you are both providing the configuration
                              and state dictionary (resp. with keyword arguments
                              `config` and `state_dict`).
                    force_download (`bool`, *optional*, defaults to `False`):
                        Whether to force the (re-)download of the model weights
                        and configuration files, overriding the cached versions
                        if they exist.
                    resume_download (`bool`, *optional*, defaults to `False`):
                        Whether to delete incompletely received files. Will
                        attempt to resume the download if such a file exists.
                    proxies (`Dict[str, str]`, *optional*):
                        A dictionary of proxy servers to use by protocol or
                        endpoint, e.g., `{'http': 'foo.bar:3128',
                        'http://hostname': 'foo.bar:4012'}`. The proxies are
                        used on each request.
                    token (`str` or `bool`, *optional*):
                        The token to use as HTTP bearer authorization for remote
                        files. If `True`, will use the token generated when
                        running `transformers-cli login` (stored in
                        `~/.huggingface`).
                    cache_dir (`Union[str, os.PathLike]`, *optional*):
                        Path to a directory in which a downloaded pretrained
                        model configuration should be cached if the standard
                        cache should not be used.
                    local_files_only(`bool`, *optional*, defaults to `False`):
                        Whether to only look at local files (i.e., do not try to
                        download the model).
                    model_kwargs (`Dict`, *optional*):
                        model_kwargs will be passed to the model during
                        initialization

                <Tip>

                Passing `token=True` is required when you want to use a
                private model.

                </Tip>
        """

        model_id = pretrained_model_name_or_path



        config_file: Optional[str] = None
        if os.path.isdir(model_id):
            if CONFIG_NAME in os.listdir(model_id):
                config_file = os.path.join(model_id, CONFIG_NAME)
            else:
                logger.warning(f"{CONFIG_NAME} not found in {Path(model_id).resolve()}")
        else:
            try:
                config_file = hf_hub_download(
                    repo_id=model_id,
                    filename=CONFIG_NAME,
                    revision=revision,
                    cache_dir=cache_dir,
                    force_download=force_download,
                    proxies=proxies,
                    resume_download=resume_download,
                    token=token,
                    local_files_only=local_files_only,
                )
            except requests.exceptions.RequestException:
                logger.warning(f"{CONFIG_NAME} not found in HuggingFace Hub")

        if config_file is not None:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            model_kwargs.update({"config": config})

        return cls._from_pretrained(
            model_id,
            revision,
            cache_dir,
            force_download,
            proxies,
            resume_download,
            local_files_only,
            token,
            **model_kwargs,
        )

    @validate_hf_hub_args
    def push_to_hub(
            self,
            # NOTE: deprecated signature that will change in 0.12
            *,
            repo_path_or_name: Optional[str] = None,
            repo_url: Optional[str] = None,
            commit_message: str = "Add model",
            organization: Optional[str] = None,
            private: bool = False,
            api_endpoint: Optional[str] = None,
            token: Optional[str] = None,
            git_user: Optional[str] = None,
            git_email: Optional[str] = None,
            config: Optional[dict] = None,
            skip_lfs_files: bool = False,
            # NOTE: New arguments since 0.9
            repo_id: Optional[str] = None,  # optional only until 0.12
            branch: Optional[str] = None,
            create_pr: Optional[bool] = None,
            allow_patterns: Optional[Union[List[str], str]] = None,
            ignore_patterns: Optional[Union[List[str], str]] = None,
            # TODO (release 0.12): signature must be the following
            # repo_id: str,
            # *,
            # commit_message: str = "Add model",
            # private: bool = False,
            # api_endpoint: Optional[str] = None,
            # token: Optional[str] = None,
            # branch: Optional[str] = None,
            # create_pr: Optional[bool] = None,
            # config: Optional[dict] = None,
            # allow_patterns: Optional[Union[List[str], str]] = None,
            # ignore_patterns: Optional[Union[List[str], str]] = None,
    ) -> str:
        """
        Upload model checkpoint to the Hub.

        Use `allow_patterns` and `ignore_patterns` to precisely filter which files
        should be pushed to the hub. See [`upload_folder`] reference for more details.

        Parameters:
            repo_id (`str`, *optional*):
                Repository name to which push.
            commit_message (`str`, *optional*):
                Message to commit while pushing.
            private (`bool`, *optional*, defaults to `False`):
                Whether the repository created should be private.
            api_endpoint (`str`, *optional*):
                The API endpoint to use when pushing the model to the hub.
            token (`str`, *optional*):
                The token to use as HTTP bearer authorization for remote files.
                If not set, will use the token set when logging in with
                `transformers-cli login` (stored in `~/.huggingface`).
            branch (`str`, *optional*):
                The git branch on which to push the model. This defaults to
                the default branch as specified in your repository, which
                defaults to `"main"`.
            create_pr (`boolean`, *optional*):
                Whether or not to create a Pull Request from `branch` with that commit.
                Defaults to `False`.
            config (`dict`, *optional*):
                Configuration object to be saved alongside the model weights.
            allow_patterns (`List[str]` or `str`, *optional*):
                If provided, only files matching at least one pattern are pushed.
            ignore_patterns (`List[str]` or `str`, *optional*):
                If provided, files matching any of the patterns are not pushed.

        Returns:
            The url of the commit of your model in the given repository.
        """
        # If the repo id is set, it means we use the new version using HTTP endpoint
        # (introduced in v0.9).
        if repo_id is not None:
            api = HfApi(endpoint=api_endpoint)
            api.create_repo(
                repo_id=repo_id,
                repo_type="model",
                token=token,
                private=private,
                exist_ok=True,
            )

            # Push the files to the repo in a single commit
            with tempfile.TemporaryDirectory() as tmp:
                saved_path = Path(tmp) / repo_id
                self.save_pretrained(saved_path, config=config)
                return api.upload_folder(
                    repo_id=repo_id,
                    repo_type="model",
                    token=token,
                    folder_path=saved_path,
                    commit_message=commit_message,
                    revision=branch,
                    create_pr=create_pr,
                    allow_patterns=allow_patterns,
                    ignore_patterns=ignore_patterns,
                )

        # If the repo id is None, it means we use the deprecated version using Git
        # TODO: remove code between here and `return repo.git_push()` in release 0.12
        if repo_path_or_name is None and repo_url is None:
            raise ValueError(
                "You need to specify a `repo_path_or_name` or a `repo_url`."
            )

        if token is None and repo_url is None:
            token = HfFolder.get_token()
            if token is None:
                raise ValueError(
                    "You must login to the Hugging Face hub on this computer by typing"
                    " `huggingface-cli login` and entering your credentials to use"
                    " `token=True`. Alternatively, you can pass your own token"
                    " as the `token` argument."
                )
        elif isinstance(token, str):
            token = token
        else:
            token = None

        if repo_path_or_name is None:
            assert repo_url is not None, "A `None` repo URL would have raised above"
            repo_path_or_name = repo_url.split("/")[-1]

        # If no URL is passed and there's no path to a directory containing files, create a repo
        if repo_url is None and not os.path.exists(repo_path_or_name):
            repo_id = Path(repo_path_or_name).name
            if organization:
                repo_id = f"{organization}/{repo_id}"
            repo_url = HfApi(endpoint=api_endpoint).create_repo(
                repo_id=repo_id,
                token=token,
                private=private,
                repo_type=None,
                exist_ok=True,
            )

        repo = Repository(
            repo_path_or_name,
            clone_from=repo_url,
            token=token,
            git_user=git_user,
            git_email=git_email,
            skip_lfs_files=skip_lfs_files,
        )
        repo.git_pull(rebase=True)

        # Save the files in the cloned repo
        self.save_pretrained(repo_path_or_name, config=config)

        # Commit and push!
        repo.git_add(auto_lfs_track=True)
        repo.git_commit(commit_message)
        return repo.git_push()


    def _save_pretrained(self, save_directory):
        """
        Overwrite this method if you wish to save specific layers instead of the
        complete model.
        """
        path = os.path.join(save_directory, PYTORCH_WEIGHTS_NAME)
        model_to_save = self.module if hasattr(self, "module") else self
        torch.save(model_to_save.state_dict(), path)

    @classmethod
    def _from_pretrained(
            cls,
            model_id,
            revision,
            cache_dir,
            force_download,
            proxies,
            resume_download,
            local_files_only,
            token,
            map_location="cpu",
            strict=False,
            **model_kwargs,
    ):
        """
        Overwrite this method to initialize your model in a different way.
        """
        map_location = torch.device(map_location)

        if os.path.isdir(model_id):
            print("Loading weights from local directory")
            model_file = os.path.join(model_id, PYTORCH_WEIGHTS_NAME)
        else:
            model_file = hf_hub_download(
                repo_id=model_id,
                filename=PYTORCH_WEIGHTS_NAME,
                revision=revision,
                cache_dir=cache_dir,
                force_download=force_download,
                proxies=proxies,
                resume_download=resume_download,
                token=token,
                local_files_only=local_files_only,
            )
        model = cls(**model_kwargs)

        state_dict = torch.load(model_file, map_location=map_location)
        model.load_state_dict(state_dict, strict=strict)
        model.eval()

        return model

    @add_start_docstrings_to_model_forward(BART_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=Seq2SeqLMOutput, config_class=_CONFIG_FOR_DOC)
    @add_end_docstrings(BART_GENERATION_EXAMPLE)
    def forward(
            self,
            input_ids: torch.LongTensor = None,
            attention_mask: Optional[torch.Tensor] = None,
            decoder_input_ids: Optional[torch.LongTensor] = None,
            decoder_attention_mask: Optional[torch.LongTensor] = None,
            head_mask: Optional[torch.Tensor] = None,
            decoder_head_mask: Optional[torch.Tensor] = None,
            cross_attn_head_mask: Optional[torch.Tensor] = None,
            encoder_outputs: Optional[List[torch.FloatTensor]] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            decoder_inputs_embeds: Optional[torch.FloatTensor] = None,
            labels: Optional[torch.LongTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, Seq2SeqLMOutput]:
        r"""
        labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
            Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
            config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
            (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.
        Returns:
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if labels is not None:
            if use_cache:
                logger.warning("The `use_cache` argument is changed to `False` since `labels` is provided.")
            use_cache = False
            if decoder_input_ids is None and decoder_inputs_embeds is None:
                decoder_input_ids = shift_tokens_right(
                    labels, self.config.pad_token_id, self.config.decoder_start_token_id
                )

        outputs = self.model(
            input_ids,
            attention_mask=attention_mask,
            decoder_input_ids=decoder_input_ids,
            encoder_outputs=encoder_outputs,
            decoder_attention_mask=decoder_attention_mask,
            head_mask=head_mask,
            decoder_head_mask=decoder_head_mask,
            cross_attn_head_mask=cross_attn_head_mask,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            decoder_inputs_embeds=decoder_inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        lm_logits = self.lm_head(outputs[0]) + self.final_logits_bias

        masked_lm_loss = None
        if labels is not None:
            loss_fct = CrossEntropyLoss()
            masked_lm_loss = loss_fct(lm_logits.view(-1, self.config.vocab_size), labels.view(-1))

        if not return_dict:
            output = (lm_logits,) + outputs[1:]
            return ((masked_lm_loss,) + output) if masked_lm_loss is not None else output

        return Seq2SeqLMOutput(
            loss=masked_lm_loss,
            logits=lm_logits,
            past_key_values=outputs.past_key_values,
            decoder_hidden_states=outputs.decoder_hidden_states,
            decoder_attentions=outputs.decoder_attentions,
            cross_attentions=outputs.cross_attentions,
            encoder_last_hidden_state=outputs.encoder_last_hidden_state,
            encoder_hidden_states=outputs.encoder_hidden_states,
            encoder_attentions=outputs.encoder_attentions,
        )



class BartDecoderPlus(BartDecoder):
    def __init__(self,keyBart:BartForConditionalGeneration,adapter_hid_dim: int) -> None:
        super().__init__(keyBart.get_decoder().config)
        self.decoder = keyBart.model.decoder
        self.adapters = nn.ModuleList([Adapter(self.decoder.config.d_model,adapter_hid_dim) for _ in range(len(self.decoder.layers))])
        self.config = self.decoder.config
        self.dropout = self.decoder.dropout
        self.layerdrop = self.decoder.layerdrop
        self.padding_idx = self.decoder.padding_idx
        self.max_target_positions = self.decoder.max_target_positions
        self.embed_scale = self.decoder.embed_scale
        self.embed_tokens = self.decoder.embed_tokens
        self.embed_positions = self.decoder.embed_positions
        self.layers = self.decoder.layers
        self.layernorm_embedding = self.decoder.layernorm_embedding
        self.gradient_checkpointing = self.decoder.gradient_checkpointing


    def forward(
            self,
            input_ids: torch.LongTensor = None,
            attention_mask: Optional[torch.Tensor] = None,
            encoder_hidden_states: Optional[torch.FloatTensor] = None,
            encoder_attention_mask: Optional[torch.LongTensor] = None,
            head_mask: Optional[torch.Tensor] = None,
            cross_attn_head_mask: Optional[torch.Tensor] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, BaseModelOutputWithPastAndCrossAttentions]:
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # retrieve input_ids and inputs_embeds
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both decoder_input_ids and decoder_inputs_embeds at the same time")
        elif input_ids is not None:
            input = input_ids
            input_shape = input.shape
            input_ids = input_ids.view(-1, input_shape[-1])
        elif inputs_embeds is not None:
            input_shape = inputs_embeds.size()[:-1]
            input = inputs_embeds[:, :, -1]
        else:
            raise ValueError("You have to specify either decoder_input_ids or decoder_inputs_embeds")

        # past_key_values_length
        past_key_values_length = past_key_values[0][0].shape[2] if past_key_values is not None else 0

        if inputs_embeds is None:
            inputs_embeds = self.decoder.embed_tokens(input) * self.decoder.embed_scale

        attention_mask = self.decoder._prepare_decoder_attention_mask(
            attention_mask, input_shape, inputs_embeds, past_key_values_length
        )

        # expand encoder attention mask
        if encoder_hidden_states is not None and encoder_attention_mask is not None:
            # [bsz, seq_len] -> [bsz, 1, tgt_seq_len, src_seq_len]
            encoder_attention_mask = _expand_mask(encoder_attention_mask, inputs_embeds.dtype, tgt_len=input_shape[-1])

        # embed positions
        positions = self.decoder.embed_positions(input, past_key_values_length)

        hidden_states = inputs_embeds + positions
        hidden_states = self.decoder.layernorm_embedding(hidden_states)

        hidden_states = nn.functional.dropout(hidden_states, p=self.decoder.dropout, training=self.decoder.training)

        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        all_cross_attentions = () if (output_attentions and encoder_hidden_states is not None) else None
        next_decoder_cache = () if use_cache else None

        # check if head_mask/cross_attn_head_mask has a correct number of layers specified if desired
        for attn_mask, mask_name in zip([head_mask, cross_attn_head_mask], ["head_mask", "cross_attn_head_mask"]):
            if attn_mask is not None:
                if attn_mask.size()[0] != (len(self.decoder.layers)):
                    raise ValueError(
                        f"The `{mask_name}` should be specified for {len(self.decoder.layers)} layers, but it is for"
                        f" {head_mask.size()[0]}."
                    )

        for idx, decoder_layer in enumerate(self.decoder.layers):
            # add LayerDrop (see https://arxiv.org/abs/1909.11556 for description)
            if output_hidden_states:
                all_hidden_states += (hidden_states,)
            dropout_probability = random.uniform(0, 1)
            if self.decoder.training and (dropout_probability < self.decoder.layerdrop):
                continue

            past_key_value = past_key_values[idx] if past_key_values is not None else None

            if self.decoder.gradient_checkpointing and self.decoder.training:

                if use_cache:
                    logger.warning(
                        "`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`..."
                    )
                    use_cache = False

                def create_custom_forward(module):
                    def custom_forward(*inputs):
                        # None for past_key_value
                        return module(*inputs, output_attentions, use_cache)

                    return custom_forward

                layer_outputs = torch.utils.checkpoint.checkpoint(
                    create_custom_forward(decoder_layer),
                    hidden_states,
                    attention_mask,
                    encoder_hidden_states,
                    encoder_attention_mask,
                    head_mask[idx] if head_mask is not None else None,
                    cross_attn_head_mask[idx] if cross_attn_head_mask is not None else None,
                    None,
                )
            else:

                layer_outputs = decoder_layer(
                    hidden_states,
                    attention_mask=attention_mask,
                    encoder_hidden_states=encoder_hidden_states,
                    encoder_attention_mask=encoder_attention_mask,
                    layer_head_mask=(head_mask[idx] if head_mask is not None else None),
                    cross_attn_layer_head_mask=(
                        cross_attn_head_mask[idx] if cross_attn_head_mask is not None else None
                    ),
                    past_key_value=past_key_value,
                    output_attentions=output_attentions,
                    use_cache=use_cache,
                )
            hidden_states = layer_outputs[0]

            ######################### new #################################
            hidden_states = self.adapters[idx](hidden_states)
            ######################### new #################################

            if use_cache:
                next_decoder_cache += (layer_outputs[3 if output_attentions else 1],)

            if output_attentions:
                all_self_attns += (layer_outputs[1],)

                if encoder_hidden_states is not None:
                    all_cross_attentions += (layer_outputs[2],)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        next_cache = next_decoder_cache if use_cache else None
        if not return_dict:
            return tuple(
                v
                for v in [hidden_states, next_cache, all_hidden_states, all_self_attns, all_cross_attentions]
                if v is not None
            )
        return BaseModelOutputWithPastAndCrossAttentions(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
            cross_attentions=all_cross_attentions,
        )

class BartPlus(BartModel):
    def __init__(self,keyBart: BartForConditionalGeneration, adapter_hid_dim: int ) -> None:
        super().__init__(keyBart.model.config)
        self.config = keyBart.model.config

        self.shared = keyBart.model.shared
        self.encoder = keyBart.model.encoder
        self.decoder = BartDecoderPlus(keyBart,adapter_hid_dim=adapter_hid_dim)

    def forward(
            self,
            input_ids: torch.LongTensor = None,
            attention_mask: Optional[torch.Tensor] = None,
            decoder_input_ids: Optional[torch.LongTensor] = None,
            decoder_attention_mask: Optional[torch.LongTensor] = None,
            head_mask: Optional[torch.Tensor] = None,
            decoder_head_mask: Optional[torch.Tensor] = None,
            cross_attn_head_mask: Optional[torch.Tensor] = None,
            encoder_outputs: Optional[List[torch.FloatTensor]] = None,
            past_key_values: Optional[List[torch.FloatTensor]] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            decoder_inputs_embeds: Optional[torch.FloatTensor] = None,
            use_cache: Optional[bool] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple, Seq2SeqModelOutput]:

        # different to other models, Bart automatically creates decoder_input_ids from
        # input_ids if no decoder_input_ids are provided
        if decoder_input_ids is None and decoder_inputs_embeds is None:
            if input_ids is None:
                raise ValueError(
                    "If no `decoder_input_ids` or `decoder_inputs_embeds` are "
                    "passed, `input_ids` cannot be `None`. Please pass either "
                    "`input_ids` or `decoder_input_ids` or `decoder_inputs_embeds`."
                )

            decoder_input_ids = shift_tokens_right(
                input_ids, self.config.pad_token_id, self.config.decoder_start_token_id
            )

        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if encoder_outputs is None:
            encoder_outputs = self.encoder(
                input_ids=input_ids,
                attention_mask=attention_mask,
                head_mask=head_mask,
                inputs_embeds=inputs_embeds,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=return_dict,
            )
        # If the user passed a tuple for encoder_outputs, we wrap it in a BaseModelOutput when return_dict=True
        elif return_dict and not isinstance(encoder_outputs, BaseModelOutput):
            encoder_outputs = BaseModelOutput(
                last_hidden_state=encoder_outputs[0],
                hidden_states=encoder_outputs[1] if len(encoder_outputs) > 1 else None,
                attentions=encoder_outputs[2] if len(encoder_outputs) > 2 else None,
            )

        # decoder outputs consists of (dec_features, past_key_value, dec_hidden, dec_attn)
        decoder_outputs = self.decoder(
            input_ids=decoder_input_ids,
            attention_mask=decoder_attention_mask,
            encoder_hidden_states=encoder_outputs[0],
            encoder_attention_mask=attention_mask,
            head_mask=decoder_head_mask,
            cross_attn_head_mask=cross_attn_head_mask,
            past_key_values=past_key_values,
            inputs_embeds=decoder_inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        if not return_dict:
            return decoder_outputs + encoder_outputs

        return Seq2SeqModelOutput(
            last_hidden_state=decoder_outputs.last_hidden_state,
            past_key_values=decoder_outputs.past_key_values,
            decoder_hidden_states=decoder_outputs.hidden_states,
            decoder_attentions=decoder_outputs.attentions,
            cross_attentions=decoder_outputs.cross_attentions,
            encoder_last_hidden_state=encoder_outputs.last_hidden_state,
            encoder_hidden_states=encoder_outputs.hidden_states,
            encoder_attentions=encoder_outputs.attentions,
        )

