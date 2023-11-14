import os
from notion_client import Client


def read_markdown_file(filepath):
    with open(filepath, "r") as file:
        return file.read()


def clear_page_blocks(notion, page_id):
    # ページ内の既存のブロックを取得
    existing_blocks = notion.blocks.children.list(page_id)["results"]

    # 既存の各ブロックを削除
    for block in existing_blocks:
        notion.blocks.delete(block["id"])


def update_notion_page(notion, page_id, content):
    # ページの既存のブロックをクリア
    clear_page_blocks(notion, page_id)

    # Markdownの内容をNotionページに追加
    # ここではシンプルなテキストブロックとして追加していますが、
    # 実際にはMarkdownをNotionのブロックに変換する必要があります。
    notion.blocks.children.append(
        page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}],
                },
            }
        ],
    )


def main():
    notion_token = os.environ.get("NOTION_TOKEN")
    notion_page_id = os.environ.get("NOTION_PAGE_ID")
    markdown_file_path = "../qa/sheet.md"  # Markdownファイルのパス

    # Notionクライアントの初期化
    notion = Client(auth=notion_token)

    # Markdownファイルの読み込み
    markdown_content = read_markdown_file(markdown_file_path)

    # Notionページの更新
    update_notion_page(notion, notion_page_id, markdown_content)


if __name__ == "__main__":
    main()
