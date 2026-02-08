for neon db:
psql 'postgresql://hackton-backend_owner:Gbo52kKyPEjl@ep-weathered-breeze-a53lrhrn-pooler.us-east-2.aws.neon.tech/hackton-backend?sslmode=require&channel_binding=require'

claude mcp add --transport stdio context7 npx @upstash/context7-mcp
claude mcp add --transport http better-auth https://mcp.chonkie.ai/better-auth/better-auth-builder/mcp
claude mcp add --transport http vercel https://mcp.vercel.com
claude mcp add --transport stdio playwright npx @playwright/mcp@latest