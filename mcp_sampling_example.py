"""
MCP Sampling Implementation Example
=====================================

Setting up sampling requires code on both sides:
    1. Server Side - the tool function that requests text generation
    2. Client Side - the callback that handles the server's requests

"""

# =====================================================================
# SERVER SIDE
# =====================================================================
# In your tool function, use the `create_message` function to request
# text generation:

@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    prompt = f"""
    Please summarize the following text:
    {text_to_summarize}
    """
    
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=prompt
                )
            )
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant",
    )
    
    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")


# =====================================================================
# CLIENT SIDE
# =====================================================================
# Create a sampling callback that handles the server's requests:

async def sampling_callback(
    context: RequestContext, params: CreateMessageRequestParams
):
    # Call Claude using the Anthropic SDK
    text = await chat(params.messages)
    
    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )


# ---------------------------------------------------------------------
# Then pass this callback when initializing your client session:
# ---------------------------------------------------------------------

async with ClientSession(
    read,
    write,
    sampling_callback=sampling_callback
) as session:
    await session.initialize()
