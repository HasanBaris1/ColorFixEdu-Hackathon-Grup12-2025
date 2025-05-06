import requests

def send_request_to_google_ai(api_key: str, input_data: dict):
    """
    Google AI Studio API'ye istek gönderir ve yanıtı döner.

    Args:
        api_key (str): Google AI Studio API anahtarı.
        input_data (dict): API'ye gönderilecek veri.

    Returns:
        dict: API'den dönen yanıt.
    """
    url = "https://api.googleaistudio.com/v1/endpoint"  # Google AI Studio'nun gerçek endpoint URL'sini buraya ekleyin
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=input_data)
        response.raise_for_status()  # Hata durumunda bir istisna fırlatır
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def send_image_to_google_ai(api_key: str, image_path: str):
    """
    Google AI Studio API'ye bir resim gönderir ve yanıtı döner.

    Args:
        api_key (str): Google AI Studio API anahtarı.
        image_path (str): Gönderilecek resmin dosya yolu.

    Returns:
        dict: API'den dönen yanıt.
    """
    url = "https://api.googleaistudio.com/v1/image-endpoint"  # Google AI Studio'nun gerçek endpoint URL'sini buraya ekleyin
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()  # Hata durumunda bir istisna fırlatır
            return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except FileNotFoundError:
        return {"error": "Resim dosyası bulunamadı!"}

# Örnek kullanım
if __name__ == "__main__":
    api_key = "your_google_ai_api_key"  # API anahtarınızı buraya ekleyin
    input_data = {"input": "örnek veri"}  # Gönderilecek veriyi buraya ekleyin

    result = send_request_to_google_ai(api_key, input_data)
    print(result)

    image_path = "path_to_your_image.jpg"  # Gönderilecek resmin dosya yolunu buraya ekleyin

    result = send_image_to_google_ai(api_key, image_path)
    print(result)
