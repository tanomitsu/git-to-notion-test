import { Client } from '@notionhq/client'
import { markdownToBlocks } from '@tryfabric/martian'
import * as fs from 'fs'
import dotenv from 'dotenv'

dotenv.config()

// GitHub Actionsの環境変数を使用
const notionToken = process.env.NOTION_TOKEN
const pageId = process.env.NOTION_PAGE_ID

async function updateNotionPage(
  notionToken: string,
  pageId: string,
  markdownFilePath: string
) {
  const notion = new Client({ auth: notionToken })
  const markdownContent = fs.readFileSync(markdownFilePath, 'utf8')
  const blocks = markdownToBlocks(markdownContent)

  // 既存のブロックをクリア
  const existingBlocks = await notion.blocks.children.list({
    block_id: pageId,
  })
  for (const block of existingBlocks.results) {
    await notion.blocks.delete({ block_id: block.id })
  }

  // 新しいブロックを追加
  await notion.blocks.children.append({
    block_id: pageId,
    children: blocks as any,
  })
}

async function main() {
  const markdownFilePath = 'qa/sheet.md'

  if (!notionToken) {
    throw new Error('NOTION_TOKEN is not set.')
  }
  if (!pageId) {
    throw new Error('NOTION_PAGE_ID is not set.')
  }

  updateNotionPage(notionToken, pageId, markdownFilePath)
}

main()
