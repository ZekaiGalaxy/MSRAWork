# pip install kittycad
from typing import Any, List, Optional, Tuple, Union
from kittycad.api.ai import create_text_to_cad
from kittycad.client import ClientFromEnv
from kittycad.models import Error, TextToCad
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.text_to_cad_create_body import TextToCadCreateBody
from kittycad.types import Response
from kittycad.client import Client
from kittycad.api.ai import get_text_to_cad_model_for_user
from kittycad.types import Response
import base64

client = Client(token="018c96c0-0282-7522-ba5a-4ae6d433553d")

def example_create_text_to_cad(prompt):
    global client
    result: Optional[Union[TextToCad, Error]] = create_text_to_cad.sync(
        client=client,
        output_format=FileExportFormat.OBJ,
        body=TextToCadCreateBody(
            prompt=prompt,
        ),
    )

    if isinstance(result, Error) or result == None:
        print(result)
        raise Exception("Error in response")

    obj: TextToCad = result
    print(obj)
    return obj

# obj = example_create_text_to_cad("chair")

def example_get_text_to_cad_model_for_user(id):
    global client
    result: Optional[
        Union[TextToCad, Error]
    ] = get_text_to_cad_model_for_user.sync(
        client=client,
        id=id,
    )

    if isinstance(result, Error) or result == None:
        print(result)
        raise Exception("Error in response")

    body: TextToCad = result
    print(body)
    return body

id = "e0e7e996-6a45-477e-9209-efeda4cb8add"
base64id = "<kittycad.models.base64data.Base64Data object at 0x7f855830b760>"
# body = example_get_text_to_cad_model_for_user(uid)

def base64_to_file(base64_data_obj):
    base64_encoded_data = base64_data_obj.some_property_or_method()
    decoded_data = base64.b64decode(base64_encoded_data)
    with open('output_file.obj', 'wb') as file:
        file.write(decoded_data)

base64_to_file(base64id)



