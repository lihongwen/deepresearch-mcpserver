# MCP Server for Deep Research

MCP Server for Deep Research is a powerful tool designed for conducting comprehensive research on complex topics. It helps you explore questions in depth, find relevant sources, and generate structured research reports with proper citations.

🔬 Your personal AI Research Assistant - turning complex research questions into comprehensive, well-cited reports.

## ✨ What's New

This fork includes enhanced features:
- 🛠️ **Direct Tool Access**: Call the `start_deep_research` tool directly from Claude Desktop
- 📊 **Structured Research Workflow**: Guided process from question elaboration to final report
- 🌐 **Web Search Integration**: Leverages Claude's built-in search capabilities
- 📝 **Professional Reports**: Generates well-formatted research reports as artifacts

## 🚀 Quick Start

### Prerequisites
- [Claude Desktop](https://claude.ai/download)
- Python 3.10 or higher
- `uv` package manager

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/lihongwen/deepresearch-mcpserver.git
   cd deepresearch-mcpserver
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure Claude Desktop**
   
   Edit your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   
   Add the following configuration:
   ```json
   {
     "mcpServers": {
       "mcp-server-deep-research": {
         "command": "uv",
         "args": [
           "--directory",
           "/path/to/your/deepresearch-mcpserver",
           "run",
           "mcp-server-deep-research"
         ]
       }
     }
   }
   ```

4. **Restart Claude Desktop**

5. **Start Researching**
   - Use the prompt template: "Start deep research on [your question]"
   - Or call the `start_deep_research` tool directly
   - Watch as Claude conducts comprehensive research and generates a detailed report

## 🎯 Features

The Deep Research MCP Server offers a complete research workflow:

### 1. **Question Elaboration**
   - Expands and clarifies your research question
   - Identifies key terms and concepts
   - Defines scope and parameters
   - Considers multiple perspectives

### 2. **Subquestion Generation**
   - Creates 3-5 focused subquestions that address different aspects
   - Ensures comprehensive coverage of the main topic
   - Provides structure for systematic research
   - Breaks down complex topics into manageable components

### 3. **Web Search Integration**
   - Uses Claude's built-in web search capabilities
   - Performs targeted searches for each subquestion
   - Identifies relevant and authoritative sources
   - Collects diverse perspectives on the topic
   - Searches multiple sources per subquestion

### 4. **Content Analysis**
   - Evaluates information quality and relevance
   - Assesses source credibility
   - Synthesizes findings from multiple sources
   - Identifies patterns and contradictions
   - Provides proper citations for all sources

### 5. **Report Generation**
   - Creates well-structured, comprehensive reports as artifacts
   - Properly cites all sources with URLs
   - Presents a balanced view with evidence-based conclusions
   - Uses appropriate formatting (tables, lists, headings)
   - Includes executive summaries and conclusions
   - Acknowledges limitations and areas of uncertainty

## 💡 Usage Example

```
User: "请直接调用research工具来进行研究 - 分析人工智能在医疗领域的应用前景"

Claude will:
1. Elaborate the question and identify key aspects
2. Generate subquestions (e.g., current applications, challenges, future trends)
3. Search for relevant information for each subquestion
4. Analyze and synthesize the findings
5. Generate a comprehensive research report with citations
```

## 🔧 How It Works

1. **Call the Tool**: Invoke `start_deep_research` with your research question
2. **Follow the Workflow**: Claude follows a structured research process
3. **Review the Report**: Get a comprehensive report as an artifact
4. **Cite Sources**: All information is properly cited with source URLs

## 📦 Components

### Tools
- **start_deep_research**: Initiates a comprehensive research workflow on any topic
  - Input: `research_question` (string)
  - Output: Structured research guidance and workflow

### Prompts
- **deep-research**: Pre-configured prompt template for starting research tasks

### Resources
- Dynamic research state tracking
- Progress notes and findings storage

## ⚙️ Configuration

### Claude Desktop Config Locations
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Development Setup (Local)
```json
{
  "mcpServers": {
    "mcp-server-deep-research": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YourUsername\\path\\to\\deepresearch-mcpserver",
        "run",
        "mcp-server-deep-research"
      ]
    }
  }
}
```

### Production Setup (Published)
If published to PyPI:
```json
{
  "mcpServers": {
    "mcp-server-deep-research": {
      "command": "uvx",
      "args": [
        "mcp-server-deep-research"
      ]
    }
  }
}
```

## 🛠️ Development

### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/lihongwen/deepresearch-mcpserver.git
cd deepresearch-mcpserver

# Install dependencies
uv sync

# Run in development mode
uv run mcp-server-deep-research
```

### Testing
```bash
# Install the MCP Inspector for testing
npx @modelcontextprotocol/inspector uv --directory . run mcp-server-deep-research
```

### Building and Publishing
1. **Sync Dependencies**
   ```bash
   uv sync
   ```

2. **Build Distributions**
   ```bash
   uv build
   ```
   Generates source and wheel distributions in the `dist/` directory.

3. **Publish to PyPI** (if you have publishing rights)
   ```bash
   uv publish
   ```

### Project Structure
```
deepresearch-mcpserver/
├── src/
│   └── mcp_server_deep_research/
│       ├── __init__.py
│       └── server.py           # Main MCP server implementation
├── pyproject.toml              # Project configuration
├── README.md                   # This file
└── LICENSE                     # MIT License
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🐛 **Report Bugs**: Open an issue describing the bug
2. 💡 **Suggest Features**: Share your ideas for improvements
3. 🔧 **Submit Pull Requests**: Fix bugs or add features
4. 📖 **Improve Documentation**: Help make the docs better

### Contribution Guidelines
- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Write clear commit messages

## 📝 Changelog

### Latest Updates
- ✅ Added `start_deep_research` tool for direct invocation
- ✅ Enhanced research workflow with structured prompts
- ✅ Improved error handling and logging
- ✅ Updated documentation with examples

## 🙏 Acknowledgments

This project is based on the original [mcp-server-deep-research](https://github.com/reading-plus-ai/mcp-server-deep-research) by reading-plus-ai.

Special thanks to:
- Anthropic for the MCP protocol and Claude AI
- The open-source community for inspiration and support

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/lihongwen/deepresearch-mcpserver
- **Issues**: https://github.com/lihongwen/deepresearch-mcpserver/issues
- **MCP Protocol**: https://modelcontextprotocol.io
- **Claude Desktop**: https://claude.ai/download

---

**Made with ❤️ for better AI-powered research**
