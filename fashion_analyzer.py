import base64
from pathlib import Path
from typing import List, Optional

from openai import OpenAI
from pydantic import BaseModel


class FashionItem(BaseModel):
    item_type: str  # トップス、ボトムス、ジャンパーなど
    size: Optional[str]  # サイズ情報
    brand: Optional[str]  # ブランド名


class ImageDirectoryError(Exception):
    """画像ディレクトリに関するエラー"""

    pass


def encode_image(image_path: str) -> str:
    """画像をBase64エンコードする"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_image_files(directory: str) -> List[Path]:
    """指定されたディレクトリから画像ファイルを取得する"""
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    directory_path = Path(directory)

    if not directory_path.exists():
        raise ImageDirectoryError(f"ディレクトリが存在しません: {directory}")
    if not directory_path.is_dir():
        raise ImageDirectoryError(f"指定されたパスはディレクトリではありません: {directory}")

    image_files = [f for f in directory_path.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]

    if not image_files:
        raise ImageDirectoryError(f"指定されたディレクトリ {directory} に画像ファイルが見つかりません")

    return image_files


def analyze_fashion_images(image_paths: List[Path]) -> FashionItem:
    """複数の画像から服飾アイテムを分析し、詳細情報を返す"""
    client = OpenAI()

    # 全ての画像をBase64エンコード
    content = [
        {
            "type": "text",
            "text": "これらの画像は同じ服飾アイテムを異なる角度から撮影したものです。全ての画像を総合的に分析して、アイテムの詳細情報を抽出してください。",
        }
    ]

    # 各画像をコンテンツに追加
    for image_path in image_paths:
        base64_image = encode_image(str(image_path))
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})

    # プロンプトの設定
    system_prompt = """
    あなたは服飾アイテムを分析する専門家です。
    提供される複数の画像は、同じアイテムを異なる角度から撮影したものです。
    全ての画像を総合的に分析し、以下の情報を抽出してください：
    1. アイテムの種類（トップス、ボトムス、ジャンパーなど）
    2. サイズ情報（タグから読み取れる場合。ただし、複数サイズ記載されている場合はUSAサイズを優先する）
    3. ブランド名（タグや特徴から判断できる場合）
    
    不明な情報がある場合は、nullとして返してください。
    複数の画像から得られる情報を組み合わせて、より正確な分析を行ってください。
    """

    # APIリクエスト
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
        response_format=FashionItem,
        max_tokens=300,
    )

    return response.choices[0].message.parsed


def analyze_directory(directory: str = "images") -> FashionItem:
    """ディレクトリ内の全ての画像をまとめて分析する"""
    try:
        image_files = get_image_files(directory)
        print(f"\n{len(image_files)}枚の画像を分析します...")

        result = analyze_fashion_images(image_files)

        print("\n=== 分析結果 ===")
        print(f"アイテムタイプ: {result.item_type}")
        print(f"サイズ: {result.size or '不明'}")
        print(f"ブランド: {result.brand or '不明'}")

        return result

    except ImageDirectoryError as e:
        print(f"ディレクトリエラー: {e}")
        raise
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        raise


def main():
    try:
        # デフォルトでimagesディレクトリを使用
        directory = input("画像ディレクトリを指定してください（デフォルト: images）: ").strip() or "images"
        analyze_directory(directory)

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
