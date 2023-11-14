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
