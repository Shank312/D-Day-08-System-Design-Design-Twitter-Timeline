

# API Reference

See `api/openapi.yml` for full spec.

## Examples

### Create Tweet
```bash
curl -X POST http://localhost:8080/tweets \
  -H "Content-Type: application/json" \
  -d @api/examples/post_tweet.json
