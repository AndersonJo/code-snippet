from ray import serve
from starlette.requests import Request
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class Translator:
    def __init__(self):
        # Load model
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_1.2B")
        self.tokenizer.src_lang = 'en'

        self.model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_1.2B")
        self.model.eval()

    def translate(self, text: str) -> str:
        dest_lang_id = self.tokenizer.get_lang_id('ko')
        encoded_src = self.tokenizer(text, return_tensors="pt")
        generated_tokens = self.model.generate(**encoded_src,
                                               forced_bos_token_id=dest_lang_id,
                                               max_length=200,
                                               use_cache=True)
        result = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return result

    async def __call__(self, http_request: Request) -> str:
        korean_text: str = await http_request.json()
        return self.translate(korean_text)


translator = Translator.bind()

# if __name__ == '__main__':
#     translator = Translator()
#     print(translator.translate('self-belief and hard work will always earn you success'))
