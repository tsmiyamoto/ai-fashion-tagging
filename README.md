# AI Fashion Tagging

ファッションアイテムの画像を解析し、以下の情報を自動で抽出するツールです：
- アイテムタイプ（トップス、ボトムス、ジャンパーなど）
- サイズ情報
- ブランド名

## セットアップ手順

### 1. uvのインストール

uvは高速なPythonパッケージマネージャーです。以下のコマンドでインストールできます：

```bash
# Homebrewを使用する場合
brew install uv

# pipを使用する場合
pip install uv
```

### 2. プロジェクトのセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/tsmiyamoto/ai-fashion-tagging.git
cd ai-fashion-tagging
```

### 3. OpenAI APIキーの設定

1. [OpenAIのウェブサイト](https://platform.openai.com/)でアカウントを作成し、APIキーを取得

2. 環境変数の設定:

```bash
# macOS/Linux
export OPENAI_API_KEY="your_api_key_here"
```

## 使用方法

1. 解析したい服飾アイテムの画像を`images`ディレクトリに配置
   - 1つのアイテムにつき複数の角度から撮影した画像を用意
   - サイズタグやブランドタグの画像も含めると、より正確な結果が得られます

2. スクリプトの実行:

```bash
uv run fashion_analyzer.py
```

3. プロンプトが表示されたら、画像が格納されているディレクトリを指定
   - デフォルトでは`images`ディレクトリが使用されます


> [!NOTE] 
> ディレクトリ内のすべての画像を1アイテムとして扱うため、別のアイテムの画像をアップロードする場合は`images2`などディレクトリを分けてください

## 対応画像フォーマット

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

## 注意事項

- OpenAI APIの使用には料金が発生します
- GPT-4o miniを使用しているため、適切な課金設定が必要です
- 画像は自動的にBase64エンコードされてAPIに送信されます
