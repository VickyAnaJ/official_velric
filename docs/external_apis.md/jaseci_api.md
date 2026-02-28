Welcome to Jac#

The Only Language You Need to Build Anything

Jac is a programming language designed for humans and AI to build together. It supersets Python and JavaScript with native compilation support, adding constructs that let you weave AI into your code, model complex domains as graphs, and deploy to the cloud -- all without switching languages, managing databases, or writing infrastructure. Jac imagines what should be abstracted away from the developer and automates it through the compiler and runtime.

# A complete full-stack AI app in one file

node Todo {
    
has title: str, done: bool = False;
}

enum Category { WORK, PERSONAL, SHOPPING, HEALTH, OTHER }

def categorize(title: str) -> Category
    
by llm();

def:pub get_todos -> list {
    
if not [root-->](?:Todo) {
        
root ++> Todo(title="Buy groceries");
        
root ++> Todo(title="Finish report");
    
}
    
return [{"title": t.title, "category": str(categorize(t.title)).split(".")[-1]}
            
for t in [root-->](?:Todo)];
}

cl def:pub app() -> JsxElement {
    
has items: list = [];
    
async can with entry { items = await get_todos(); }
    
return <div>{[<p key={i.title}>{i.title} ({i.category})</p>
                  
for i in items]}</div>;
}

This single file defines a persistent data model, an AI-powered categorizer, a REST API, and a React frontend. No database setup. No prompt engineering. No separate frontend project. Just Jac.
You can actually run this example

The Vision#

Programming today demands too much from developers that isn't their problem to solve. You want to build a product, but first you have to pick a backend language, a frontend framework, a database, an ORM, a deployment target, and then glue them all together. If you want AI, add prompt engineering to the list. If you want scale, add DevOps.

Jac takes a different approach: move complexity out of the developer's code and into the language runtime. The things that can be automated -- database schemas, API serialization, client-server communication, prompt construction, deployment orchestration -- should be automated. The developer should focus on what the application does, not how the plumbing works.

This philosophy rests on three pillars.
Three Pillars#

    One Language

    Write frontend, backend, and native code in a single language. Jac's codespace system lets you target the server (sv), browser (cl), or native binary (na) from the same file. The compiler handles interop -- HTTP calls, serialization, type sharing -- so you never write glue code.

    How Codespaces Work ·
    Full-Stack Reference ·
    See Jac vs a Traditional Stack

    AI Native

    Integrate LLMs at the language level with by llm() -- the compiler extracts semantics from your function names, types, and sem annotations to construct prompts automatically. First-class graphs and walkers give you an expressive agentic programming model where AI agents traverse structured state spaces with tool-calling built in.

    How by/sem Work ·
    AI Integration Reference ·
    Agentic Patterns

    Scale Native

    Your code doesn't change when you move from laptop to cloud. Declare node types and connect them to root -- the runtime handles persistence automatically. Run jac start --scale and your app deploys to Kubernetes with Redis, MongoDB, load balancing, and health checks provisioned for you. Zero DevOps.

    How Persistence Works ·
    Deployment Reference ·
    jac-scale Plugin

One Language: Frontend, Backend, Native#

Jac introduces codespaces -- regions of code that target different execution environments. Instead of maintaining separate projects in separate languages, you write everything in Jac and the compiler produces the right output for each target:
Codespace 	Target 	Ecosystem 	Syntax
Server 	Python runtime 	PyPI (numpy, pandas, fastapi) 	sv { } or .sv.jac
Client 	Browser/JavaScript 	npm (react, tailwind, @mui) 	cl { } or .cl.jac
Native 	Compiled binary 	C ABI 	na { } or .na.jac

Server definitions are visible to client blocks. When the client calls a server function, the compiler generates the HTTP request, serialization, and routing automatically. You write one language; the compiler produces the interop layer.

See it in action

Want to see exactly how much code Jac eliminates? Check out Jac vs Traditional Stack -- a side-by-side comparison showing ~30 lines of Jac vs >300 lines of Python + FastAPI + SQLite + TypeScript + React for the same Todo app.
AI Native: LLMs as Code Constructs#

Jac's approach to AI is called Meaning Typed Programming. Instead of writing prompts in strings and parsing responses manually, you declare what you want through function signatures and let the compiler handle the how:

# The function name, types, and return type ARE the specification
def classify_sentiment(text: str) -> str by llm;

# Enums constrain the LLM to valid outputs
enum Priority { LOW, MEDIUM, HIGH, CRITICAL }
def triage_ticket(description: str) -> Priority by llm();

# sem provides additional semantic context where names aren't enough
obj Ingredient {
    
has name: str, cost: float, carby: bool;
}
sem Ingredient.cost = "Estimated cost in USD";
sem Ingredient.carby = "True if high in carbohydrates";

def plan_shopping(recipe: str) -> list[Ingredient] by llm();

The return type serves as the output contract -- enum means the LLM can only produce one of its values, obj means every field must be filled. No parsing code. No validation code. The type system enforces correctness.

For agentic workflows, Jac's graph constructs (nodes, edges, walkers) naturally model AI agents that traverse structured state spaces, make decisions with by llm(), and call tools:

def get_weather(city: str) -> str { return fetch_weather_api(city); }
def search_web(query: str) -> list[str] { return web_search_api(query); }

# The LLM decides which tools to call and in what order
def answer_question(question: str) -> str
    
by llm(tools=[get_weather, search_web]);

byLLM Quickstart Tutorial ·
Agentic AI Tutorial
Scale Native: No Code Changes from Laptop to Cloud#

Every Jac program has a built-in root node. Nodes reachable from root are persistent -- they survive process restarts. The runtime generates storage schemas from your node declarations. You never write database code:

node Todo { has title: str, done: bool = False; }

with entry {
    
root ++> Todo(title="Learn Jac");  # Automatically persisted
}

This same program runs three ways with no code changes:
Command 	What Happens
jac app.jac 	Runs locally, SQLite persistence
jac start app.jac 	HTTP API server, walkers become REST endpoints
jac start --scale 	Kubernetes deployment with Redis, MongoDB, load balancing

The runtime handles database schemas, user authentication (per-user graph isolation), API generation (Swagger docs at /docs), caching tiers, and Kubernetes orchestration. You write application logic; the runtime handles infrastructure.

Production Deployment Tutorial ·
Kubernetes Tutorial
Get Started in 5 Minutes#
Step 1: Install#

pip
 install jaseci

This installs the complete Jac ecosystem: jaclang (compiler), byllm (AI integration), jac-client (frontend), jac-scale (deployment), and jac-super (enhanced console).

Verify your installation:

jac
 --version

This also warms the cache, making subsequent commands faster.
Step 2: Create Your First Program#

Create hello.jac:

with entry {
    
print("Hello from Jac!");
}

Step 3: Run It#

jac
 hello.jac

Note: jac is shorthand for jac run -- both work identically.

That's it! You just ran your first Jac program.
Choose Your Path#

    Just want to try it?

    Follow the Installation guide to get set up and run your first program in 2 minutes.

    Building a web app?

    Jump to Build an AI Day Planner -- a complete 7-part tutorial covering backend, frontend, persistence, auth, and AI.

    Working with AI/LLMs?

    Start with the byLLM Quickstart, then explore Agentic AI for tool-calling agents and multi-agent systems.

    Interested in graphs and OSP?

    Read What Makes Jac Different for the concepts, then the OSP Tutorial for hands-on practice with nodes, edges, and walkers.

Who is Jac For?#

Jac is designed for developers who want to build AI-powered applications without the complexity of managing multiple languages and tools. If you've ever wished you could write your frontend, backend, AI logic, and deployment config in one place -- Jac is for you.
You Are 	Jac Gives You
Startup Founder 	Ship complete products faster -- one language, one deploy command
AI/ML Engineer 	Native LLM integration without prompt engineering overhead
Full-Stack Developer 	React frontend + Python backend, no context switching
Python Developer 	Familiar syntax with powerful new capabilities (Jac supersets Python)
Student/Learner 	Modern language designed for clarity, with clean syntax AI models can read and write

What You Should Know

Jac supersets Python, so Python familiarity is assumed throughout these docs. If you plan to use the full-stack features, basic React/JSX knowledge helps. No graph database experience is needed -- Jac teaches you that.
Quick Links#
Resource 	Description
Installation 	Setup, first program, scaffolding, and Jacpacks
What Makes Jac Different 	The three core concepts: codespaces, OSP, and AI integration
Syntax Cheatsheet 	Comprehensive syntax reference
Build an AI Day Planner 	Complete 7-part tutorial covering all Jac features
Language Reference 	Complete language documentation
CLI Reference 	All jac commands
FAQ 	Learning paths by experience level
Need Help?#

    Discord: Join our community server for questions and discussions
    GitHub: Report issues at Jaseci-Labs/jaseci
    JacGPT: Ask questions at jac-gpt.jaseci.org


Installation and First Run#

Get Jac installed and ready to use in under 2 minutes.
One-Line Install (Recommended)#

Install Jac with a single command -- no Python setup required:

curl
 -fsSL https://raw.githubusercontent.com/jaseci-labs/jaseci/main/scripts/install.sh | bash

This automatically installs uv (if needed), a Python 3.12+ runtime, and the full Jac ecosystem including all plugins.
Installer Options#

Pass flags after -- to customize the install:

# Core language only (no plugins)
curl
 -fsSL https://raw.githubusercontent.com/jaseci-labs/jaseci/main/scripts/install.sh | bash -s -- --core

# Specific version
curl
 -fsSL https://raw.githubusercontent.com/jaseci-labs/jaseci/main/scripts/install.sh | bash -s -- --version 2.3.1

# Standalone binary (self-contained, no Python/uv needed at runtime)
curl
 -fsSL https://raw.githubusercontent.com/jaseci-labs/jaseci/main/scripts/install.sh | bash -s -- --standalone

# Uninstall
curl
 -fsSL https://raw.githubusercontent.com/jaseci-labs/jaseci/main/scripts/install.sh | bash -s -- --uninstall

Flag 	Description
--core 	Install only the Jac language compiler, no plugins
--standalone 	Download a pre-built binary from GitHub Releases
--version V 	Install a specific version
--uninstall 	Remove Jac
Upgrading#

Re-run the install command to upgrade to the latest version. The installer detects existing installations and upgrades in place.
Install via pip#

If you already have Python 3.12+ and prefer pip:

pip
 install jaseci

The jaseci package is a meta-package that bundles all Jac ecosystem packages together. This installs:

    jaclang - The Jac language and compiler
    byllm - AI/LLM integration
    jac-client - Full-stack web development
    jac-scale - Production deployment
    jac-super - Enhanced console output

Verify the installation:

jac
 --version

This also warms the cache, making subsequent commands faster.
Installation Options#
Minimal Install (Language Only)#

If you only need the core language:

pip
 install jaclang

Individual Plugins#

Install plugins as needed:

# AI/LLM integration
pip
 install byllm

# Full-stack web development
pip
 install jac-client

# Production deployment & scaling
pip
 install jac-scale

# Enhanced console output
pip
 install jac-super

Virtual Environment (Recommended)#

# Create environment
python
 -m venv jac-env

# Activate it
source jac-env/bin/activate   # Linux/Mac
jac-env
\Scripts\activate      # Windows

# Install Jac
pip
 install jaseci

IDE Setup#
VS Code (Recommended)#

Install the official Jac extension for the best development experience:

Option 1: From Marketplace

    Open VS Code
    Click Extensions in the sidebar (or press Ctrl+Shift+X / Cmd+Shift+X)
    Search for "Jac"
    Click Install on "Jac Language Support" by Jaseci Labs

Or install directly: Open in VS Code Marketplace

Option 2: Quick Install

Press Ctrl+P / Cmd+P and paste:

ext install jaseci-labs.jaclang-extension

Features:

    Syntax highlighting for .jac files
    Intelligent autocomplete
    Real-time error detection
    Hover documentation
    Go to definition
    Graph visualization

Cursor#

    Download the latest .vsix from GitHub releases
    Press Ctrl+Shift+P / Cmd+Shift+P
    Select "Extensions: Install from VSIX"
    Choose the downloaded file

Verify Installation#

jac
 --version

Expected output:

   _
  (_) __ _  ___     Jac Language
  | |/ _` |/ __|
  | | (_| | (__     Version:  0.X.X
 _/ |\__,_|\___|    Python 3.12.3
|__/                Platform: Linux x86_64

📚 Documentation: https://docs.jaseci.org
💬 Community:     https://discord.gg/6j3QNdtcN6
🐛 Issues:        https://github.com/Jaseci-Labs/jaseci/issues

Run your first program to confirm everything works. Create hello.jac:

with entry {
    
print("Hello from Jac!");
}

jac
 hello.jac

You should see Hello from Jac! printed to the console.
Scaffold a Full-Stack App#

With the jac-client plugin installed, scaffold a complete full-stack project in one command:

jac
 create example --use fullstack
cd example
jac
 add
jac
 start main.jac

This creates a project with a Jac backend and a React frontend, ready to go at http://localhost:8000.
Community Jacpacks#

Jacpacks are ready-made Jac project templates you can spin up instantly. Since --use accepts a URL, you can run any jacpack directly from GitHub:

jac
 create my-todo --use https://raw.githubusercontent.com/jaseci-labs/jacpacks/main/multi-user-todo-app/multi-user-todo-app.jacpack
cd my-todo
jac
 add
jac
 start main.jac

Want to try one with AI built in? The multi-user-todo-meals-app uses Jac's AI integration features to generate smart shopping lists with costs and nutritional info. It works out of the box with an Anthropic API key:

export ANTHROPIC_API_KEY="your-key-here"
jac
 create meals-app --use https://raw.githubusercontent.com/jaseci-labs/jacpacks/main/multi-user-todo-meals-app/multi-user-todo-meals-app.jacpack
cd meals-app
jac
 add
jac
 start main.jac

To use any of the other jacpacks, just swap the URL:

jac
 create my-app --use https://raw.githubusercontent.com/jaseci-labs/jacpacks/main/<jacpack-name>/<jacpack-name>.jacpack

Upgrading Jac#

If you installed via the one-line installer, re-run it to upgrade:

curl
 -fsSL https://raw.githubusercontent.com/jaseci-labs/jaseci/main/scripts/install.sh | bash

If you installed via pip:

# Upgrade everything at once
pip
 install --upgrade jaseci

# Or upgrade individual packages
pip
 install --upgrade jaclang
pip
 install --upgrade byllm
pip
 install --upgrade jac-client
pip
 install --upgrade jac-scale
pip
 install --upgrade jac-super

Creating a Project#

Use jac create to scaffold a new project:

# Full-stack web app (frontend + backend)
jac
 create my-app --use client

# Start the development server
cd my-app
jac
 start main.jac

The --use client template sets up a complete project with:

    main.jac -- Entry point with server and client code
    jac.toml -- Project configuration
    styles.css -- Default stylesheet
    Bundled frontend dependencies (via Bun)

Available templates:
Template 	Command 	What It Creates
Client 	--use client 	Full-stack web app with frontend and backend
Fullstack 	--use fullstack 	Alias for --use client

You can also use community templates (Jacpacks):

jac
 create my-app --use <github-url>

For Contributors#

See the Contributing Guide for development setup.
Next Steps#

    Core Concepts - Codespaces, OSP, and compiler-integrated AI
    Build an AI Day Planner - Build a complete full-stack application

Core Concepts#

Most of Jac will be recognizable if you are familiar with another programming language like Python -- Jac supersets Python, so familiar constructs like functions, classes, imports, list comprehensions, and control flow all work as expected. You can explore those in depth in the language reference.

This page focuses on the three concepts that Jac adds beyond traditional programming languages. These are the ideas the rest of the documentation builds on, introduced briefly so you have the vocabulary for the tutorials that follow. Through these concepts three important questions can be answered:

    How can one language target frontend, backend, and native binaries at the same time?
    How does Jac fully abstract away database organization and interactions and the complexity of multiuser persistent data?
    How does Jac abstract away the laborious task of prompt/context engineering for AI and turn it into a compiler/runtime problem?

1. How can one language target frontends, backends, and native binaries at the same time?#

Similar to namespaces, the Jac language introduces the concept of codespaces. A Jac program can contain code that runs in different environments. You denote the codespace either with a block prefix inside a file or with a file extension:

main.jac

Server (PyPI Ecosystem)
sv { }

Client (NPM Ecosystem)
cl { }

Native (C ABI)
na { }

Inline blocks -- mix codespaces in a single file:

    sv { } -- code that runs on the server (compiles to Python)
    cl { } -- code that runs in the browser (compiles to JavaScript)
    na { } -- code that runs natively compiled on the host machine (compiles to native binary)
    Code outside any block defaults to the server codespace

File extensions -- set the default top-level codespace for a file, e.g., for a module prog:

    prog.sv.jac -- top-level code defaults to server
    prog.cl.jac -- top-level code defaults to client
    prog.na.jac -- top-level code defaults to native
    prog.jac -- defaults to the server codespace

Any .jac file can still use all codespace blocks regardless of its extension. The extension only changes what the default is for code outside any block.

Here's a file that uses two codespaces via inline blocks:

# Server codespace (default)
node Todo {
    
has title: str, done: bool = False;
}

def:pub add_todo(title: str) -> dict {
    
todo = root ++> Todo(title=title);
    
return {"id": todo[0].id, "title": todo[0].title};
}

# Client codespace
cl {
    
def:pub app -> JsxElement {
        
has items: list = [];

        
async def add -> None {
            
todo = await add_todo("New");
            
items = items + [todo];
        
}

        
return <div>
            <button onClick={lambda -> None { add(); }}>
                Add
            </button>
        </div>;
    
}
}

The server definitions are visible to the cl block. When the client calls add_todo(...), the compiler generates the HTTP call, serialization, and routing between codespaces. You write one language; the compiler produces the interop layer.

Codespaces are similar to namespaces, but instead of organizing names, they organize where code executes. Interop between them -- function calls, spawn calls, type sharing -- is handled by the compiler and runtime.
2. How does Jac fully abstract away database organization and interactions and the complexity of multiuser persistent data?#

Most languages store data in variables, objects, or database rows -- and you're responsible for the ORM, the schema, and the queries. Jac adds another option: nodes that live in a graph. You declare your data, connect it, and the runtime handles persistence automatically.

A node is declared like an obj/class, but with a superpower -- nodes can be connected to other nodes with edges, forming a graph:

node Task {
    
has title: str;
    
has done: bool = False;
}

with entry {
    
# Create tasks and connect them to root
    
root ++> Task(title="Buy groceries");
    
root ++> Task(title="Team standup at 10am");
    
root ++> Task(title="Go for a run");
}

The ++> operator creates a node and connects it to an existing node with an edge. Your graph now looks like:

root

Task("Buy groceries")

Task("Team standup at 10am")

Task("Go for a run")
Persistence through root#

Every Jac program has a built-in root node. Nodes reachable from root are persistent -- they survive process restarts. The runtime generates the storage schema from your node declarations automatically. No database setup, no ORM, no SQL.

When your app serves multiple users, each user gets their own isolated root. User A's tasks and User B's tasks live in completely separate graphs -- same code, isolated data, enforced by the runtime.
Querying the graph#

The [-->] syntax gives you a list of connected nodes, and Jac's filter comprehensions (?...) let you narrow the results:

with entry {
    
# Get all nodes connected from root as a list
    
everything = [root-->];

    
# Filter by node type
    
tasks = [root-->](?:Task);

    
# Filter by field value
    
pending = [root-->](?:Task, done == False);
}

Edges can also be typed with their own data, modeling relationships like schedules, dependencies, or social connections:

edge Scheduled {
    
has time: str;
    
has priority: int = 1;
}

with entry {
    
root +>: Scheduled(time="9:00am", priority=3) :+> Task(title="Morning run");

    
# Query through typed edges
    
urgent = [root->:Scheduled:priority>=3:->](?:Task);
}

The key insight: instead of designing database tables and writing queries, you declare nodes and connect them. The graph is your data model, and root is the entry point. The runtime takes care of the rest.
3. How does Jac abstract away the laborious task of prompt/context engineering for AI and turn it into a compiler/runtime problem?#

Jac introduces Compiler-Integrated AI through its by and sem keywords. These two keywords allow integrating language models into programs at the language level rather than through library calls.
by -- delegate a function's implementation#

enum Category { WORK, PERSONAL, SHOPPING, HEALTH, OTHER }

def categorize(title: str) -> Category
    
by llm();

This function has no body. by llm() tells the compiler to delegate the implementation to a language model. The compiler extracts semantics from the code itself -- the function name, parameter names, types, and return type -- to construct the prompt. A well-named function like categorize with a typed parameter title: str and return type Category already communicates intent.

The return type is enforced. If the return type is an enum, the LLM can only produce one of its values. If it's an obj, every field must be filled. The type annotation serves as the output contract.
sem -- attach semantics to bindings#

The compiler can only infer so much from names and types. sem is the mechanism for providing additional semantic information beyond what exists in the code. It attaches a description to a specific variable binding that the compiler includes in the prompt:

obj Ingredient {
    
has name: str;
    
has cost: float;
    
has carby: bool;
}

sem Ingredient.cost = "Estimated cost in USD";
sem Ingredient.carby = "True if this ingredient is high in carbohydrates";

def plan_shopping(recipe: str) -> list[Ingredient]
    
by llm();
sem plan_shopping = "Generate a shopping list for the given recipe.";

Without sem, the LLM has only the names cost and carby to work with. With it, the compiler includes "Estimated cost in USD" and "True if this ingredient is high in carbohydrates" in the prompt, producing more accurate structured output. The sem on plan_shopping itself provides the function-level instruction.

sem is not a comment. It's a compiler directive that attaches semantic meaning to variable bindings -- fields, parameters, functions -- and changes what the LLM sees at runtime. It is the only way to convey intent beyond what the compiler can extract from the code and values in the program.
How the Three Concepts Relate#

    Codespaces define where code runs -- server, client, or native
    OSP defines how data is structured and traversed -- nodes, edges, walkers, and persistence through root
    by and sem define how AI is integrated -- the compiler extracts semantics from code structure, and sem provides additional meaning where names and types aren't sufficient

In practice, these compose: walkers traverse a graph on the server, delegate decisions to an LLM via by llm(), and the results render in a client-side UI -- all within one language.
Quick Reference#
Syntax 	Meaning
sv { } 	Server codespace
cl { } 	Client codespace
na { } 	Native codespace
node X { has ...; } 	Declare a graph data type
root 	Built-in starting node (persistence anchor)
a ++> b 	Connect node a to node b
[a -->] 	Get all nodes connected from a
walker W { } 	Declare mobile computation
visit [-->] 	Move walker to connected nodes
by llm() 	Delegate function body to an LLM
sem X.field = "..." 	Semantic hint for AI understanding
Next Steps#

    Jac vs Traditional Stack -- Side-by-side comparison with a traditional stack
    Build an AI Day Planner -- Apply these concepts in a working app
    Object-Spatial Programming -- Full tutorial on nodes, edges, and walkers
    byLLM Quickstart -- Build an AI-integrated function


Build an AI Day Planner with Jac#

In this tutorial, you'll build a full-stack AI day planner from scratch -- a single application that manages daily tasks (auto-categorized by AI) and generates meal shopping lists from natural language descriptions. Each part introduces new concepts incrementally, so by the end you'll have hands-on experience with every major feature of the Jac programming language.

Prerequisites: Installation complete.

Required Packages: This tutorial uses jaclang, jac-client, jac-scale, and byllm. Install everything at once with:

pip
 install jaseci

Verify your versions meet the minimum requirements:

jac
 --version
pip
 show jac-client jac-scale byllm

Package 	Minimum Version
jaclang 	0.11.0
jac-client 	0.3.0
jac-scale 	0.2.0
byllm 	0.5.0

API Key: Parts 5+ use AI features powered by Anthropic's Claude. Set your API key as an environment variable before running those sections:

export ANTHROPIC_API_KEY="your-key-here"

The tutorial is split into seven parts. Each builds on the last:
Part 	What You'll Build 	Key Concepts
1 	Hello World 	Syntax basics, types, functions
2 	Task data model 	Nodes, graphs, root, edges
3 	Backend API 	def:pub, imports, collections, list comprehensions
4 	Working frontend 	Client-side code, lambdas, JSX, reactive state
5 	AI features 	by llm(), obj, sem, structured output
6 	Authentication 	Login, signup, def:priv, per-user data, multi-file
7 	Walkers & OSP 	Walkers, abilities, graph traversal
Part 1: Your First Lines of Jac#

Before building anything complex, it's important to get comfortable with Jac's syntax. Jac is a programming language whose compiler can generate Python bytecode, ES JavaScript, and native binaries. Its design is rooted in Python, so if you have Python experience, much of Jac will feel familiar -- but there are deliberate differences: curly braces replace indentation for block scoping, semicolons terminate statements, and the language has built-in support for graphs, AI, and full-stack web development. The goal of this section is to give you a solid foundation in the basics so that everything that follows feels natural.

Hello, World

Create a file called hello.jac:

with entry {
    
print("Hello, World!");
}

Run it:

jac
 hello.jac

In Jac, any free-floating code in a module must live inside a with entry { } block. These blocks execute when you run a .jac file as a script, and also at the point it's imported -- similar to top-level code in Python. The reason Jac requires this explicit demarcation is an important design principle: code that runs once on module load is a common source of subtle bugs in larger programs. By making it visually distinct, Jac ensures you're always intentional about side effects at the module level.

Why with entry?

Python was originally designed as a replacement for bash, and its initial version didn't even have import statements. Jac slightly discourages mistakes stemming from free-floating module code by making it an intentional, visible choice in the language.

Variables and Types

Understanding Jac's type system is essential for everything that follows, especially the AI features in later parts. Jac has four basic scalar types: str, int, float, and bool. When you declare a variable with an explicit type, a type annotation is required:

with entry {
    
name: str = "My Day Planner";
    
version: int = 1;
    
rating: float = 4.5;
    
ready: bool = True;

    
# Type can be inferred from the value
    
greeting = f"Welcome to {name} v{version}!";
    
print(greeting);
}

Jac supports f-strings for string interpolation (just like Python), comments with #, and introduces block comments with #* ... *#:

# This is a line comment

#* This is a
   block comment *#

Functions

Functions in Jac use the familiar def keyword. A key difference from Python is that both parameters and return values require type annotations. This strictness pays off later -- when you delegate functions to an LLM in Part 5, the type signatures become the specification that guides the AI's output:

def greet(name: str) -> str {
    
return f"Good morning, {name}! Let's plan your day.";
}

def add(a: int, b: int) -> int {
    
return a + b;
}

with entry {
    
print(greet("Alice"));
    
print(add(2, 3));  # 5
}

Functions that don't return a value use -> None (or you can omit the return type annotation entirely).

Control Flow

Jac uses curly braces {} for all blocks, which means indentation is purely cosmetic -- there's no significant whitespace. This is a deliberate departure from Python that eliminates an entire class of formatting bugs:

def check_time(hour: int) -> str {
    
if hour < 12 {
        
return "Good morning!";
    
} elif hour < 17 {
        
return "Good afternoon!";
    
} else {
        
return "Good evening!";
    
}
}

with entry {
    
# For loop over a list
    
tasks = ["Buy groceries", "Team standup", "Go running"];
    
for task in tasks {
        
print(f"- {task}");
    
}

    
# Range-based loop
    
for i in range(5) {
        
print(i);  # 0, 1, 2, 3, 4
    
}

    
# While loop
    
count = 3;
    
while count > 0 {
        
print(f"Countdown: {count}");
        
count -= 1;
    
}

    
# Ternary expression
    
hour = 10;
    
mood = "energized" if hour < 12 else "tired";
    
print(mood);
}

Jac provides two pattern-matching constructs, each designed for a different purpose. switch/case is for classic simple value matching -- there's no fall-through and no break needed, which avoids a common source of bugs in C-family languages:

def categorize(fruit: str) -> str {
    
switch fruit {
        
case "apple":
            
return "pome";
        
case "banana" | "plantain":
            
return "berry";
        
default:
            
return "unknown";
    
}
}

match/case, on the other hand, is for Python-style structural pattern matching -- use it when you need to destructure values or match more complex patterns:

def describe(value: any) -> str {
    
match value {
        
case 0:
            
return "zero";
        
case 1 | 2 | 3:
            
return "small number";
        
case _:
            
return "something else";
    
}
}

Classes and Objects

Since Jac's design is based on Python, it supports Python-style classes directly with the class keyword. This is a good starting point if you're coming from Python, but pay attention to what comes after -- Jac offers a better alternative:

class Animal {

    
# __init__ works here too
    
def init(self: Animal, name: str, sound: str) {
        
self.name = name;
        
self.sound = sound;
    
}

    
def speak(self: Animal) -> str {
        
return f"{self.name} says {self.sound}!";
    
}
}

with entry {
    
dog = Animal("Rex", "Woof");
    
print(dog.speak());  # Rex says Woof!
}

This works, but notice the boilerplate: you must write self in every method signature, and the init method manually assigns each parameter to an instance variable. This repetitive pattern is exactly the kind of ceremony that slows down development. Jac addresses this with obj -- a first-class construct where fields declared with has are automatically initialized (like a dataclass), and self is implicitly available in methods without being listed in parameters.

Why obj?

Python's dataclass decorator was an admission that traditional classes have too much boilerplate for simple data types. Jac's obj builds this idea into the language itself. For a deeper dive, see Dataclasses: Python's Admission That Classes Are Broken.

obj Animal {
    
has name: str,
        
sound: str;

    
def speak -> str {
        
return f"{self.name} says {self.sound}!";
    
}
}

with entry {
    
dog = Animal(name="Rex", sound="Woof");
    
print(dog.speak());  # Rex says Woof!
}

Take a moment to compare the two versions. With obj, you don't write self in method signatures -- it's always available inside the body. Fields listed in has become constructor parameters automatically, so there's no init method to write for simple cases. This isn't just syntactic sugar -- it's a design philosophy: the less ceremony around data types, the more clearly your code expresses its intent. Throughout this tutorial, we'll use obj for plain data types and node (introduced in Part 2) for data that lives in the graph.

What You Learned

    with entry { } -- program entry point
    Types: str, int, float, bool
    def -- function declaration with typed parameters and return types
    Control flow: if / elif / else, for, while, switch, match -- all with braces
    class -- Python-style classes with explicit self
    obj -- Jac data types with has fields and implicit self
    # -- line comments (#* block comments *#)
    f-strings -- string interpolation with f"...{expr}..."
    Ternary -- value if condition else other

For a quick reference of all Jac syntax, see the Syntax Cheatsheet.

Try It Yourself

Write a plan_day function that takes a list of task names and an hour: int, and returns a formatted string like "Good morning! Today's tasks: Buy groceries, Go running". Use check_time for the greeting and a for loop to build the task list.
Part 2: Modeling Data with Nodes#

In most programming languages, data lives in one of a few places: local variables, object instances in memory, or rows in a database. Each has trade-offs -- variables are temporary, objects require manual serialization to persist, and databases demand configuration, schemas, and query languages. Jac introduces a fundamentally different option: nodes that live in a graph and persist automatically. There's no database to set up, no ORM to configure, and no SQL to write. The goal of this section is to help you understand graphs as a first-class citizen of the language and see how the traditional database layer can disappear entirely.

What is a Node?

A node is structurally similar to an obj -- it's declared with the node keyword and its fields use has, just like you learned in Part 1. The difference is what the runtime does with it:

node Task {
    
has id: str,
        
title: str,
        
done: bool = False;
}

The syntax looks almost identical to an obj, but nodes have a crucial additional capability: they can be connected to other nodes with edges (also obj-style classes), forming a graph. Think about the difference this makes. In traditional programming, objects exist independently in memory -- relationships between them must be maintained manually through references, foreign keys, or join tables. In Jac, relationships are structural. Objects are connected, and those connections form first-class graphs in the language.

This becomes especially powerful when coupled with one more abstraction: the self-referential root.

The Root Node and the Graph

Every Jac program has a built-in root node -- the entry point of the graph. This is a concept worth pausing on, because it's central to how Jac works. Just as self in an object method is a self-referential pointer to the current instance, root is a self-referential pointer to the current runner of the program -- whether that's you executing a script or an authenticated user making a request. And like self, root is ambiently available everywhere; you never import or declare it, it's just there in every code block. Think of it as the top of a tree of everything that should persist:

root

Here's the key insight: any node connected to root (directly or through a chain of edges) is persistent -- it survives across requests, program runs, and server restarts. You don't configure a database or write SQL; connecting a node to root is the declaration that it should be saved. This is a fundamentally different model from traditional persistence, where you explicitly serialize data to a database. In Jac, persistence is a property of graph connectivity. Nodes that are not reachable from root behave like regular objects -- they live in memory for the duration of the current execution and are then garbage collected, though you can still connect them to other nodes for utility while they exist.

When your app serves multiple users, each user gets their own isolated root. User A's tasks and User B's tasks live in completely separate graphs -- same code, isolated data, enforced by the runtime. Connections between user graphs are possible when explicitly created, but by default each user's root is a private, independent entry point. We'll see this in action in Part 6 when we add authentication.

Now that you understand the concept, let's see it in practice by creating nodes and connecting them with edges.

Creating and Connecting Nodes

The ++> operator creates a node and connects it to an existing node with an edge. This single operator does what would typically require multiple steps in traditional code: instantiating an object, saving it to a database, and creating a foreign key relationship:

node Task {
    
has id: str,
        
title: str,
        
done: bool = False;
}

with entry {
    
# Create tasks and connect them to root
    
root ++> Task(id="1", title="Buy groceries");
    
root ++> Task(id="2", title="Team standup at 10am");
    
root ++> Task(id="3", title="Go for a run");

    
print("Created 3 tasks!");
}

Run it with jac <your-filename>.jac. Your graph now looks like:

Running examples multiple times

Nodes connected to root persist between runs. If you run an example again, you'll see duplicate data. To start fresh, run jac clean --all to clear the graph database.

root

Task("Buy groceries")

Task("Team standup at 10am")

Task("Go for a run")

The ++> operator returns a list containing the newly created node. You can capture it:

result = root ++> Task(id="1", title="Buy groceries");
task = result[0];  # The new Task node
print(task.title);  # "Buy groceries"

Filter Comprehensions

Before querying the graph, it's worth learning a Jac feature that works on any collection of objects, not just graph queries: filter comprehensions. Understanding this distinction is important -- filter comprehensions are a general-purpose tool that happens to work beautifully with graph queries. The (?...) syntax filters a list by field conditions, and (?:Type) filters by type:

obj Dog { has name: str, age: int; }
obj Cat { has name: str, age: int; }

with entry {
    
pets: list = [
        
Dog(name="Rex", age=5),
        
Cat(name="Whiskers", age=3),
        
Dog(name="Buddy", age=2)
    
];

    
# Filter by type -- keep only Dogs
    
dogs = pets(?:Dog);
    
print(dogs);  # [Dog(name='Rex', age=5), Dog(name='Buddy', age=2)]

    
# Filter by field condition
    
young = pets(?age < 4);
    
print(young);  # [Cat(name='Whiskers', age=3), Dog(name='Buddy', age=2)]

    
# Combined type + field filter
    
young_dogs = pets(?:Dog, age < 4);
    
print(young_dogs);  # [Dog(name='Buddy', age=2)]
}

This works on any list of objects -- not just graph queries. That's important for what comes next.

Querying the Graph

Now here's where the two concepts come together. The [-->] syntax gives you a list of connected nodes -- and because filter comprehensions work on any list, they apply to graph queries seamlessly:

with entry {
    
root ++> Task(id="1", title="Buy groceries");
    
root ++> Task(id="2", title="Team standup at 10am");

    
# Get ALL nodes connected from root
    
everything = [root-->];

    
# Filter by node type -- same (?:Type) syntax
    
tasks = [root-->](?:Task);
    
for task in tasks {
        
status = "done" if task.done else "pending";
        
print(f"[{status}] {task.title}");
    
}

    
# Filter by field value
    
grocery_tasks = [root-->](?:Task, title == "Buy groceries");
}

[root-->] reads as "all nodes connected from root." The (?:Task) filter keeps only nodes of type Task. Notice the elegance of this design: there's nothing special about graph queries. [-->] returns a plain list, and (?...) filters it, using the same mechanism it uses on any collection. This composability -- where general-purpose features combine naturally -- is a recurring theme in Jac.

Other directions work too:

    [node-->] -- outgoing connections (forward)
    [node<--] -- incoming connections (backward)
    [node<-->] -- both directions

Deleting Nodes

Use del to remove a node from the graph:

for task in [root-->](?:Task) {
    
if task.id == "2" {
        
del task;
    
}
}

Debugging Tip

You can inspect the graph at any time by printing connected nodes:

print([root-->]);           # All nodes connected to root
print([root-->](?:Task));   # Just Task nodes

This is useful when data isn't appearing as expected.
Advanced: Custom Edges

What You Learned

    node -- a persistent data type that lives in the graph
    has -- declares fields with types and optional defaults
    root -- the built-in entry point of the graph, self-referential to the current runner
    ++> -- create a node and connect it with an edge
    (?condition) -- filter comprehensions on any list of objects
    (?:Type) -- typed filter comprehension, works on any collection
    (?:Type, field == val) -- combined type and field filtering
    [root-->] -- query all connected nodes (returns a list, filterable like any other)
    del -- remove a node from the graph

Try It Yourself

After creating three tasks, mark one as done (task.done = True), then use [root-->](?:Task, done == False) to list only pending tasks. Verify that the completed task doesn't appear.
Part 3: Building the Backend API#

With the fundamentals of Jac syntax and graph data in place, you're now ready to build something practical. In this part, you'll create HTTP endpoints that manage tasks -- and you'll see how Jac eliminates the boilerplate that typically comes with web frameworks: no route decorators, no serializers, no request/response handling code.

Create the Project

jac
 create day-planner --use client
cd day-planner

You can delete the scaffolded main.jac -- you'll replace it with the code below. Also create a styles.css file in the project root (we'll fill it in Part 4).

Imports

An important feature of Jac is full interoperability with the Python ecosystem. You can import any Python package -- from the standard library or from PyPI. Here, we need uuid for generating unique task IDs:

import from uuid { uuid4 }

The syntax is import from module { names } -- it imports uuid4 from Python's standard library uuid module. You can import anything from PyPI the same way.

def:pub -- Functions as Endpoints

This is one of the most powerful ideas in Jac. Simply mark a function def:pub and the compiler automatically generates an HTTP endpoint for it -- complete with request parsing, response serialization, and API documentation:

"""Add a task and return it."""
def:pub add_task(title: str) -> dict {
    
task = root ++> Task(id=str(uuid4()), title=title);
    
return {"id": task[0].id, "title": task[0].title, "done": task[0].done};
}

That single annotation transforms the function into two things simultaneously:

    A server-side function you can call from Jac code
    An HTTP endpoint that clients can call over the network

Consider what this replaces in a traditional web framework: you'd need a route decorator, a request parser to extract title from the request body, serialization logic to convert the response to JSON, and error handling for malformed requests. In Jac, the function signature is the API contract. The function's parameters define the request schema, and its return type defines the response format.

Building the CRUD Endpoints

With that understanding, here are all four CRUD (Create, Read, Update, Delete) operations for managing tasks:

import from uuid { uuid4 }

node Task {
    
has id: str,
        
title: str,
        
done: bool = False;
}

"""Add a task and return it."""
def:pub add_task(title: str) -> dict {
    
task = root ++> Task(id=str(uuid4()), title=title);
    
return {"id": task[0].id, "title": task[0].title, "done": task[0].done};
}

"""Get all tasks."""
def:pub get_tasks -> list {
    
return [{"id": t.id, "title": t.title, "done": t.done} for t in [root-->](?:Task)];
}

"""Toggle a task's done status."""
def:pub toggle_task(id: str) -> dict {
    
for task in [root-->](?:Task) {
        
if task.id == id {
            
task.done = not task.done;
            
return {"id": task.id, "title": task.title, "done": task.done};
        
}
    
}
    
return {};
}

"""Delete a task."""
def:pub delete_task(id: str) -> dict {
    
for task in [root-->](?:Task) {
        
if task.id == id {
            
del task;
            
return {"deleted": id};
        
}
    
}
    
return {};
}

Before moving on, let's examine the new patterns used in this code. These are foundational data structures you'll use throughout the rest of the tutorial.

Collections

Lists work like Python -- create with [], access by index, iterate with for:

tasks = ["Buy groceries", "Go running", "Read a book"];
first = tasks[0];          # "Buy groceries"
last = tasks[-1];          # "Read a book"
length = len(tasks);       # 3
tasks.append("Cook dinner");

Dictionaries use {"key": value} syntax:

task_data = {"id": "1", "title": "Buy groceries", "done": False};
print(task_data["title"]);  # "Buy groceries"
task_data["done"] = True;   # Update a value

List comprehensions build lists in a single expression:

# Build a list of dicts from all Task nodes
[{"id": t.id, "title": t.title} for t in [root-->](?:Task)]

# With a filter condition
[t.title for t in [root-->](?:Task) if not t.done]

Run It

Even without a frontend, you can start the server and interact with your API right away. This is a good practice for verifying your backend logic works correctly before adding UI complexity:

jac
 start main.jac

The server starts on port 8000 by default. Use --port 3000 to pick a different port.

Open http://localhost:8000/docs to see Swagger UI with all your endpoints listed. You can test each one interactively -- expand an endpoint, click "Try it out", fill in the parameters, and hit "Execute." This is a great way to verify your backend works before building a frontend.

You can also visit http://localhost:8000/graph to see a visual representation of the data graph attached to root. Right now it will be empty, but once you add tasks (try it from the Swagger UI!), you'll see them appear as nodes connected to root.

jac vs jac start

In Parts 1-2 we used jac <file> to run scripts. jac start <file> launches a web server that serves def:pub endpoints and any frontend components. Use jac for scripts, jac start for web apps.

Common issue

If you see "Address already in use", another process is on that port. Use --port to pick a different one.

What You Learned

    def:pub -- functions that auto-become HTTP endpoints
    import from module { name } -- import Python (or any) packages
    List comprehensions -- [expr for x in list] and [expr for x in list if cond]
    Dictionaries -- {"key": value} for structured data
    jac start -- run the web server

Try It Yourself

Add a get_pending_tasks endpoint that returns only tasks where done is False. Hint: add an if not t.done condition to the list comprehension from get_tasks.
Part 4: A Reactive Frontend#

So far, you've been working entirely on the server side. Now you'll learn how Jac handles the frontend. Unlike most backend languages that require a separate JavaScript project for the UI, Jac can render full UIs in the browser using JSX syntax -- similar to React, but without requiring a separate JavaScript toolchain or build system.

The cl Prefix

Jac uses the cl (client) prefix to distinguish between server-side and browser-side code. Any code marked with cl is compiled to JavaScript and runs in the browser, not on the server:

cl import "./styles.css";

This loads a CSS file client-side. Add this line at the top of your main.jac, after the uuid import.

Building the Component

A cl def:pub function returning JsxElement is a UI component:

cl def:pub app -> JsxElement {
    
has tasks: list = [],
        
task_text: str = "";

    
# ... methods and render tree ...
}

Notice the has keyword appearing again -- you first saw it in obj and node declarations. Inside a component, has declares reactive state. When any of these values change, the UI automatically re-renders to reflect the new data. If you're familiar with React, this is the same concept as useState, but expressed as simple property declarations rather than hook function calls.
You can also use React's useState directly

Lifecycle Hooks

can with entry runs when the component first mounts (like React's useEffect on mount):

    
async can with entry {
        
tasks = await get_tasks();
    
}

This fetches all tasks from the server when the page loads.
You can also use React's useEffect directly

Lambdas

Before building the UI, you need to understand lambdas -- Jac's anonymous functions. These are essential for event handlers in JSX, where you need to pass small inline functions to respond to user actions like clicks and key presses:

# Lambda with typed parameters
double = lambda x: int -> int { return x * 2; };

# Lambda with no parameters
say_hi = lambda -> str { return "hi"; };

The syntax is lambda params -> return_type { body }. In JSX, you'll use them inline to handle user events:

onChange={lambda e: any -> None { task_text = e.target.value; }}

Transparent Server Calls

This is one of the most important concepts to understand in Jac's full-stack model: await add_task(text) calls the server function as if it were local code. Behind the scenes, because add_task is def:pub, Jac generated both an HTTP endpoint on the server and a matching client stub in the browser automatically. The client stub handles the HTTP request, JSON serialization, and response parsing for you. You never write fetch calls, parse JSON, or handle HTTP status codes -- the boundary between client and server becomes invisible.

    
async def add_new_task -> None {
        
if task_text.strip() {
            
task = await add_task(task_text.strip());
            
tasks = tasks + [task];
            
task_text = "";
        
}
    
}

Rendering Lists and Conditionals

{[... for t in tasks]} renders a list of elements. Each item needs a unique key prop:

{[
    
<div key={t.id} class="task-item">
        <span>{t.title}</span>
    </div> for t in tasks
]}

Conditional rendering uses Jac's ternary expression inside JSX:

<span class={"task-title " + ("task-done" if t.done else "")}>
    {t.title}
</span>

Building the Frontend Step by Step

Now that you understand the individual pieces -- reactive state, lifecycle hooks, lambdas, transparent server calls, and JSX rendering -- it's time to assemble them into a working component. Add cl import "./styles.css"; after your existing import. Start with the input, add button, and a basic task list:

cl def:pub app -> JsxElement {
    
has tasks: list = [],
        
task_text: str = "";

    
async can with entry {
        
tasks = await get_tasks();
    
}

    
async def add_new_task -> None {
        
if task_text.strip() {
            
task = await add_task(task_text.strip());
            
tasks = tasks + [task];
            
task_text = "";
        
}
    
}

    
return
        
<div class="container">
            <h1>Day Planner</h1>
            <div class="input-row">
                <input
                    class="input"
                    value={task_text}
                    onChange={lambda e: any -> None { task_text = e.target.value; }}
                    onKeyPress={lambda e: any -> None {
                        
if e.key == "Enter" { add_new_task(); }
                    
}}
                    
placeholder="What needs to be done today?"
                
/>
                
<button class="btn-add" onClick={add_new_task}>Add</button>
            
</div>
            
{[
                
<div key={t.id} class="task-item">
                    <span class="task-title">{t.title}</span>
                </div> for t in tasks
            
]}
        
</div>;
}

This is already functional -- you can type a task, press Enter, and see it appear. Take a moment to appreciate how the concepts you've learned work together: reactive has state re-renders the UI automatically when data changes, the lifecycle hook loads existing data on mount, and await add_task() transparently calls the server without any HTTP code.

Adding Toggle and Delete

Now add checkboxes, delete buttons, and a task counter. Insert these methods after add_new_task, and update the task list rendering:

cl def:pub app -> JsxElement {
    
has tasks: list = [],
        
task_text: str = "";

    
async can with entry {
        
tasks = await get_tasks();
    
}

    
async def add_new_task -> None {
        
if task_text.strip() {
            
task = await add_task(task_text.strip());
            
tasks = tasks + [task];
            
task_text = "";
        
}
    
}

    
async def toggle(id: str) -> None {
        
await toggle_task(id);
        
tasks = [
            
{"id": t.id, "title": t.title, "done": not t.done}
            
if t.id == id else t
            
for t in tasks
        
];
    
}

    
async def remove(id: str) -> None {
        
await delete_task(id);
        
tasks = [t for t in tasks if t.id != id];
    
}

    
remaining = len([t for t in tasks if not t.done]);

    
return
        
<div class="container">
            <h1>Day Planner</h1>
            <div class="input-row">
                <input
                    class="input"
                    value={task_text}
                    onChange={lambda e: any -> None { task_text = e.target.value; }}
                    onKeyPress={lambda e: any -> None {
                        
if e.key == "Enter" { add_new_task(); }
                    
}}
                    
placeholder="What needs to be done today?"
                
/>
                
<button class="btn-add" onClick={add_new_task}>Add</button>
            
</div>
            
{[
                
<div key={t.id} class="task-item">
                    <input
                        type="checkbox"
                        checked={t.done}
                        onChange={lambda -> None { toggle(t.id); }}
                    />
                    <span class={"task-title " + ("task-done" if t.done else "")}>
                        {t.title}
                    </span>
                    <button
                        class="btn-delete"
                        onClick={lambda -> None { remove(t.id); }}
                    >
                        X
                    </button>
                </div> for t in tasks
            
]}
            
<div class="count">{remaining} tasks remaining</div>
        
</div>;
}

There are several important patterns to understand in this code:

    List comprehensions transform and filter lists inline (e.g., [expr for t in tasks], [t for t in tasks if cond]). These are the same Python-style comprehensions you may already know, and they're essential for working with reactive state.
    Conditional comprehensions update matching items (e.g., [updated if t.id == id else t for t in tasks]). This pattern creates a new list where one item is modified -- crucial for immutable state updates.
    tasks + [task] creates a new list with the item appended, rather than mutating the existing list. This immutability is important because the reactive system needs to detect that the list has changed.
    async marks methods that call the server, since network calls are inherently asynchronous.

Add Styles

Now fill in styles.css in your project root:

.container { max-width: 500px; margin: 40px auto; font-family: system-ui; padding: 20px; }
h1 { text-align: center; margin-bottom: 24px; color: #333; }
.input-row { display: flex; gap: 8px; margin-bottom: 20px; }
.input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }
.btn-add { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; }
.task-item { display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee; gap: 10px; }
.task-title { flex: 1; }
.task-done { text-decoration: line-through; color: #888; }
.btn-delete { background: #e53e3e; color: white; border: none; border-radius: 4px; padding: 5px 10px; cursor: pointer; }
.count { text-align: center; color: #888; margin-top: 16px; font-size: 0.9rem; }

Run It
Complete main.jac for Parts 1–4

jac
 start main.jac

Open http://localhost:8000. You should see a clean day planner with an input field and an "Add" button. Try it:

    Type "Buy groceries" and press Enter -- the task appears
    Click the checkbox -- it gets crossed out
    Click X -- it disappears
    Stop the server and restart it -- your tasks are still there

That last point deserves emphasis. You didn't write any code to save data or load it on startup -- the data persisted automatically because the task nodes are connected to root in the graph. This is the persistence model you learned in Part 2 working seamlessly with the full-stack architecture.

Visualize the graph

Visit http://localhost:8000/graph to see your tasks as nodes connected to root. This visual view updates live as you add, toggle, and delete tasks.

What You Learned

    cl -- prefix for client-side (browser) code
    cl import -- load CSS (or npm packages) in the browser
    cl def:pub app -> JsxElement -- the main UI component
    has (in components) -- reactive state that triggers re-renders on change
    lambda -- anonymous functions: lambda params -> type { body }
    can with entry -- lifecycle hook that runs on component mount
    await func() -- transparent server calls from the client (no HTTP code)
    async -- marks functions that perform asynchronous operations
    JSX syntax -- {expression}, {[... for x in list]}, event handlers with lambdas
    List comprehensions and + operator -- [expr for x in list], [x for x in list if cond], and list + [item] for immutable state updates

Try It Yourself

Add a "Clear All" button below the task count that deletes every task. You'll need a new def:pub clear_all_tasks endpoint on the server and an async method in the component that calls it and resets the tasks list.
Part 5: Making It Smart with AI#

Your day planner works, but it doesn't leverage AI yet. This part introduces one of Jac's most distinctive capabilities: the ability to delegate functions to a large language model using nothing more than type signatures and semantic hints. You'll add two AI features -- automatic task categorization and a meal shopping list generator -- and in doing so, you'll see how Jac's type system becomes a bridge between traditional programming and AI.

Starting fresh

If you have leftover data from Parts 1–4, delete the .jac/data/ directory before running Part 5. The schema changes (adding category to Task) may conflict with old nodes.

Set Up Your API Key

Jac's AI features use an LLM under the hood. You need an API key from Anthropic (or another provider). Set it as an environment variable:

export ANTHROPIC_API_KEY="your-key-here"

Free and Alternative Models

Anthropic API keys are not free -- you'll need API credits at console.anthropic.com.

Free alternative: Use Google Gemini with Gemini API:

glob llm = Model(model_name="gemini/gemini-2.5-flash");

Self-hosted: Run models locally with Ollama:

glob llm = Model(model_name="ollama/llama3.2:1b");

Jac's AI plugin wraps LiteLLM, supporting OpenAI, Anthropic, Google, Azure, and many more.

Configure the LLM

Add the AI import and model initialization to the top of main.jac, right after the existing imports:

import from uuid { uuid4 }
import from byllm.lib { Model }
cl import "./styles.css";

glob llm = Model(model_name="claude-sonnet-4-20250514");

import from byllm.lib { Model } loads Jac's AI plugin. glob llm = Model(...) initializes the model at module level -- the glob keyword declares a module-level variable, accessible everywhere in the file.

Enums as Output Constraints

Before using AI, you need a way to constrain its output. An enum defines a fixed set of named values -- and when used as a return type for an AI function, it forces the LLM to pick from your predefined options. Access values with Category.WORK and convert to string with str(Category.WORK):

enum Category { WORK, PERSONAL, SHOPPING, HEALTH, FITNESS, OTHER }

This is a crucial concept: the enum constrains the AI to return exactly one of these predefined values. Without it, an LLM might return "shopping", "Shopping", "groceries", or "grocery shopping" -- all meaning the same thing but impossible to handle consistently in code. The enum eliminates that ambiguity entirely, making AI output as predictable as any other function return value.

by llm() -- AI Function Delegation

Now for the core idea. Pay close attention, because this pattern is central to how Jac integrates AI:

def categorize(title: str) -> Category by llm();
sem categorize = "Categorize a task based on its title";

That's the entire function. There's no body to write -- by llm() tells Jac to delegate the implementation to the LLM. The compiler constructs a prompt from everything it knows about the function:

    The function name -- categorize tells the LLM what to do
    The parameter names and types -- title: str is what the LLM receives
    The return type -- Category constrains output to one of the enum values
    The sem hint -- additional context for the LLM

This is why the type annotations you learned in Part 1 matter so much. The function name, parameter names, types, and sem hint collectively are the specification. The LLM fulfills it. In other words, the same type system that catches bugs at compile time also guides the AI at runtime.

sem vs docstrings

Use sem to provide semantic context for any declaration that the LLM needs to understand. While docstrings describe code for humans (and auto-generate API docs), sem is specifically designed to guide the LLM compiler. Always prefer sem for by llm() functions and their parameters.

Wire It Into the Task Flow

Two changes. First, add a category field to the Task node:

node Task {
    
has id: str,
        
title: str,
        
done: bool = False,
        
category: str = "other";
}

Then update add_task to call the AI:

"""Add a task with AI categorization."""
def:pub add_task(title: str) -> dict {
    
category = str(categorize(title)).split(".")[-1].lower();
    
task = root ++> Task(id=str(uuid4()), title=title, category=category);
    
return {
        
"id": task[0].id, "title": task[0].title,
        
"done": task[0].done, "category": task[0].category
    
};
}

str(categorize(title)).split(".")[-1].lower() converts Category.SHOPPING to "shopping" for clean display.

Also update get_tasks and toggle_task to include "category" in their return dictionaries:

"""Get all tasks."""
def:pub get_tasks -> list {
    
return [
        
{"id": t.id, "title": t.title, "done": t.done, "category": t.category}
        
for t in [root-->](?:Task)
    
];
}

"""Toggle a task's done status."""
def:pub toggle_task(id: str) -> dict {
    
for task in [root-->](?:Task) {
        
if task.id == id {
            
task.done = not task.done;
            
return {
                
"id": task.id, "title": task.title,
                
"done": task.done, "category": task.category
            
};
        
}
    
}
    
return {};
}

delete_task doesn't need changes -- it doesn't return task data.

Structured Output with obj and sem

Now for a more advanced use case: the shopping list. The categorize function returns a single enum value -- simple. But what if you need the AI to return structured data -- not just a string or a category, but a list of ingredients, each with a name, quantity, unit, and estimated cost? This is where obj and sem come together.

obj defines a structured data type that serves as an output schema for the LLM. Unlike node, objects aren't stored in the graph -- they're data containers that describe the shape of what the AI should return:

enum Unit { PIECE, LB, OZ, CUP, TBSP, TSP, BUNCH }

obj Ingredient {
    
has name: str;
    
has quantity: float;
    
has unit: Unit;
    
has cost: float;
    
has carby: bool;
}

sem adds a semantic hint that tells the LLM what an ambiguous field means:

sem Ingredient.cost = "Estimated cost in USD";
sem Ingredient.carby = "True if this ingredient is high in carbohydrates";

Consider why this matters: without sem, cost: float is ambiguous to the LLM -- cost in what currency? Per unit or total? Per serving? With the semantic hint, the LLM knows exactly what to generate. This is a general principle: the more precise your types and hints, the more reliable the AI output.

Now the AI function:

def generate_shopping_list(meal_description: str) -> list[Ingredient] by llm();
sem generate_shopping_list = "Generate a shopping list of ingredients needed for a described meal";

The LLM returns a list[Ingredient] -- a list of typed objects, each with name, quantity, unit, cost, and carb flag. Jac validates the structure automatically, ensuring every field has the correct type. If the LLM produces malformed output, the runtime catches it rather than letting bad data propagate through your application.

Shopping List Nodes and Endpoints

Now you need to persist the AI-generated ingredients in the graph. Notice that Ingredient (an obj) is used for AI output, while ShoppingItem (a node) is used for persistence. This separation is intentional -- the AI schema and the storage schema can evolve independently:

node ShoppingItem {
    
has name: str,
        
quantity: float,
        
unit: str,
        
cost: float,
        
carby: bool;
}

And three new endpoints:

"""Generate a shopping list from a meal description."""
def:pub generate_list(meal: str) -> list {
    
# Clear old items
    
for item in [root-->](?:ShoppingItem) {
        
del item;
    
}
    
# Generate new ones
    
ingredients = generate_shopping_list(meal);
    
result: list = [];
    
for ing in ingredients {
        
data = {
            
"name": ing.name,
            
"quantity": ing.quantity,
            
"unit": str(ing.unit).split(".")[-1].lower(),
            
"cost": ing.cost,
            
"carby": ing.carby
        
};
        
root ++> ShoppingItem(
            
name=data["name"], quantity=data["quantity"],
            
unit=data["unit"], cost=data["cost"], carby=data["carby"]
        
);
        
result.append(data);
    
}
    
return result;
}

"""Get the current shopping list."""
def:pub get_shopping_list -> list {
    
return [
        
{"name": s.name, "quantity": s.quantity, "unit": s.unit,
         
"cost": s.cost, "carby": s.carby}
        
for s in [root-->](?:ShoppingItem)
    
];
}

"""Clear the shopping list."""
def:pub clear_shopping_list -> dict {
    
for item in [root-->](?:ShoppingItem) {
        
del item;
    
}
    
return {"cleared": True};
}

Notice how generate_list clears old shopping items before generating new ones -- this ensures you always see a fresh list. The graph now holds both task and shopping data, demonstrating how different types of nodes coexist naturally:

root

Task("Buy groceries", shopping)

Task("Team standup", work)

ShoppingItem("Chicken breast", 2lb, $5.99)

ShoppingItem("Soy sauce", 2tbsp, $0.50)

Update the Frontend

The frontend needs a two-column layout: tasks on the left, shopping list on the right. Update the component with new state, methods, and the shopping panel:

cl def:pub app -> JsxElement {
    
has tasks: list = [],
        
task_text: str = "",
        
meal_text: str = "",
        
ingredients: list = [],
        
generating: bool = False;

    
async can with entry {
        
tasks = await get_tasks();
        
ingredients = await get_shopping_list();
    
}

    
async def add_new_task -> None {
        
if task_text.strip() {
            
task = await add_task(task_text.strip());
            
tasks = tasks + [task];
            
task_text = "";
        
}
    
}

    
async def toggle(id: str) -> None {
        
await toggle_task(id);
        
tasks = [
            
{
                
"id": t.id, "title": t.title,
                
"done": not t.done, "category": t.category
            
}
            
if t.id == id else t
            
for t in tasks
        
];
    
}

    
async def remove(id: str) -> None {
        
await delete_task(id);
        
tasks = [t for t in tasks if t.id != id];
    
}

    
async def generate_meal_list -> None {
        
if meal_text.strip() {
            
generating = True;
            
ingredients = await generate_list(meal_text.strip());
            
generating = False;
        
}
    
}

    
async def clear_list -> None {
        
await clear_shopping_list();
        
ingredients = [];
        
meal_text = "";
    
}

    
remaining = len([t for t in tasks if not t.done]);
    
total_cost = 0.0;
    
for ing in ingredients { total_cost = total_cost + ing.cost; }

    
return
        
<div class="container">
            <h1>AI Day Planner</h1>
            <div class="two-column">
                <div class="column">
                    <h2>Today's Tasks</h2>
                    <div class="input-row">
                        <input
                            class="input"
                            value={task_text}
                            onChange={lambda e: any -> None { task_text = e.target.value; }}
                            onKeyPress={lambda e: any -> None {
                                
if e.key == "Enter" { add_new_task(); }
                            
}}
                            
placeholder="What needs to be done today?"
                        
/>
                        
<button class="btn-add" onClick={add_new_task}>Add</button>
                    
</div>
                    
{[
                        
<div key={t.id} class="task-item">
                            <input
                                type="checkbox"
                                checked={t.done}
                                onChange={lambda -> None { toggle(t.id); }}
                            />
                            <span class={"task-title " + ("task-done" if t.done else "")}>
                                {t.title}
                            </span>
                            {(
                                
<span class="category">{t.category}</span>
                            
) if t.category and t.category != "other" else None}
                            
<button
                                class="btn-delete"
                                onClick={lambda -> None { remove(t.id); }}
                            >
                                X
                            </button>
                        
</div> for t in tasks
                    
]}
                    
<div class="count">{remaining} tasks remaining</div>
                
</div>
                
<div class="column">
                    <h2>Meal Shopping List</h2>
                    <div class="input-row">
                        <input
                            class="input"
                            value={meal_text}
                            onChange={lambda e: any -> None { meal_text = e.target.value; }}
                            onKeyPress={lambda e: any -> None {
                                
if e.key == "Enter" { generate_meal_list(); }
                            
}}
                            
placeholder="Describe a meal, e.g. 'chicken stir fry for 4'"
                        
/>
                        
<button
                            class="btn-generate"
                            onClick={generate_meal_list}
                            disabled={generating}
                        >
                            {("Generating..." if generating else "Generate")}
                        </button>
                    
</div>
                    
{(
                        
<div class="generating-msg">Generating with AI...</div>
                    
) if generating else None}
                    
{[
                        
<div key={ing.name} class="ingredient-item">
                            <div class="ing-info">
                                <span class="ing-name">{ing.name}</span>
                                <span class="ing-qty">
                                    {ing.quantity} {ing.unit}
                                </span>
                            </div>
                            <div class="ing-meta">
                                {(
                                    
<span class="carb-badge">Carbs</span>
                                
) if ing.carby else None}
                                
<span class="ing-cost">${ing.cost.toFixed(2)}</span>
                            
</div>
                        
</div> for ing in ingredients
                    
]}
                    
{(
                        
<div class="shopping-footer">
                            <span class="total">Total: ${total_cost.toFixed(2)}</span>
                            <button class="btn-clear" onClick={clear_list}>Clear</button>
                        </div>
                    
) if len(ingredients) > 0 else None}
                
</div>
            
</div>
        
</div>;
}

Update Styles

Replace styles.css with the expanded version that supports the two-column layout and shopping list:

.container { max-width: 900px; margin: 40px auto; font-family: system-ui; padding: 20px; }
h1 { text-align: center; margin-bottom: 24px; color: #333; }
h2 { margin: 0 0 16px 0; font-size: 1.2rem; color: #444; }
.two-column { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
@media (max-width: 700px) { .two-column { grid-template-columns: 1fr; } }
.input-row { display: flex; gap: 8px; margin-bottom: 16px; }
.input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; }
.btn-add { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; }
.btn-generate { padding: 10px 16px; background: #2196F3; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; white-space: nowrap; }
.btn-generate:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-delete { background: #e53e3e; color: white; border: none; border-radius: 4px; padding: 4px 8px; cursor: pointer; font-size: 0.85rem; }
.btn-clear { background: #888; color: white; border: none; border-radius: 4px; padding: 6px 12px; cursor: pointer; font-size: 0.85rem; }
.task-item { display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #eee; gap: 10px; }
.task-title { flex: 1; }
.task-done { text-decoration: line-through; color: #888; }
.category { padding: 2px 8px; background: #e8f5e9; border-radius: 12px; font-size: 0.75rem; color: #2e7d32; margin-right: 8px; }
.count { text-align: center; color: #888; margin-top: 12px; font-size: 0.9rem; }
.ingredient-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #eee; }
.ing-info { display: flex; flex-direction: column; gap: 2px; }
.ing-name { font-weight: 500; }
.ing-qty { color: #666; font-size: 0.85rem; }
.ing-meta { display: flex; align-items: center; gap: 8px; }
.ing-cost { color: #2196F3; font-weight: 600; }
.carb-badge { padding: 2px 6px; background: #fff3e0; border-radius: 12px; font-size: 0.7rem; color: #e65100; }
.shopping-footer { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; margin-top: 8px; border-top: 1px solid #ddd; }
.total { font-weight: 700; color: #2196F3; }
.generating-msg { text-align: center; padding: 20px; color: #666; }

Run It
Complete main.jac for Parts 1–5

export ANTHROPIC_API_KEY="your-key"
jac
 start main.jac

Common issue

If adding a task silently fails (nothing happens), check the terminal running jac start for error messages -- a missing or invalid API key causes a server error.

Open http://localhost:8000. The app now has two columns. Try it:

    Add "Buy groceries" -- it appears with a "shopping" badge
    Add "Schedule dentist appointment" -- tagged "health"
    Add "Review pull requests" -- tagged "work"
    Type "chicken stir fry for 4" in the meal planner and click Generate -- a structured shopping list appears with quantities, units, costs, and carb flags
    Restart the server -- everything persists (both tasks and shopping list)

The AI can only pick from the enum values you defined -- Category for tasks, Unit for ingredients. This is the key takeaway of this part: Jac's type system constrains the LLM's output automatically. You don't write prompt engineering logic or output parsers. The types are the constraints.

Visualize the graph

Visit http://localhost:8000/graph to see both Task and ShoppingItem nodes connected to root. After generating a shopping list, you'll see the graph grow with ingredient nodes alongside your tasks.

What You Learned

    import from byllm.lib { Model } -- load the AI plugin
    glob -- module-level variables, accessible throughout the file
    glob llm = Model(...) -- initialize an LLM at module level
    enum -- fixed set of named values, used here to constrain AI output
    def func(...) -> Type by llm() -- let the LLM implement a function from its signature
    obj -- structured data types (not stored in graph, used as data containers)
    sem Type.field = "..." -- semantic hints that guide LLM field interpretation
    -> list[Type] by llm() -- get validated structured output from the LLM
    Jac's type system is the LLM's output schema -- name things clearly and by llm() handles the rest

Try It Yourself

Add SOCIAL and FINANCE to the Category enum. Then test how the AI categorizes tasks like "Call mom", "Pay rent", and "Gym at 6pm".
Part 6: Authentication and Multi-File Organization#

Your day planner has AI-powered task categorization, a shopping list generator, and automatic persistence. But there's a fundamental gap: there's no concept of users. Anyone who visits the app sees the same data. In a real application, each user needs their own private data. This part teaches two important concepts: how Jac handles authentication and per-user data isolation, and how to organize a growing codebase across multiple files.

Built-in Auth

Jac has built-in authentication functions for client-side code:

import from "@jac/runtime" { jacSignup, jacLogin, jacLogout, jacIsLoggedIn }

    jacSignup(username, password) -- create an account (returns {"success": True/False})
    jacLogin(username, password) -- log in (returns True or False)
    jacLogout() -- log out
    jacIsLoggedIn() -- check login status

Authentication is often one of the most complex parts of a web application -- JWT tokens, session management, token storage, refresh logic. Jac handles all of this internally, so you can focus on your application logic rather than security plumbing.

def:priv -- Per-User Endpoints

Remember from Part 2 that root is a self-referential pointer to the current runner of the program. In Parts 3-5, you used def:pub to create public endpoints where all users shared the same root. Now that you have authentication, you want each user's data to be private. The change is remarkably simple -- replace def:pub with def:priv:

    def:pub -- public endpoint, shared data (no authentication required)
    def:priv -- private endpoint, requires authentication, operates on the user's own root

With def:priv, each authenticated user gets their own isolated graph with its own root. User A's tasks are completely invisible to User B -- same code, isolated data, enforced by the runtime. This is the payoff of the root abstraction you learned earlier: because all your code already references root rather than a global variable, switching to per-user isolation requires no changes to your business logic.

Multi-File Organization

As your application grows, keeping everything in a single file becomes hard to navigate and maintain. Jac supports splitting code across files using a declaration/implementation pattern -- a clean architectural approach that separates what a component looks like from how it behaves.

frontend.cl.jac -- state, method signatures, and the render tree:

def:pub app -> JsxElement {
    
has tasks: list = [];

    
async def fetchTasks -> None;  # Just the signature -- no body
    
# ... more declarations ...

    
# ... UI rendering ...
}

frontend.impl.jac -- method bodies in impl blocks:

impl app.fetchTasks -> None {
    
tasksLoading = True;
    
tasks = await get_tasks();
    
tasksLoading = False;
}

The .cl.jac file focuses on what the component looks like and what state it has -- think of it as the interface. The .impl.jac file focuses on what the methods do -- the implementation details. This separation is optional -- you could keep everything in one file -- but it's a best practice that pays off as your application grows, because you can understand the component's structure at a glance without scrolling through method bodies.

sv import brings server functions into client code. When a .cl.jac file calls def:priv (or def:pub) functions defined in a server module, it needs sv import so the compiler generates HTTP stubs instead of raw function calls:

sv import from main {
    
get_tasks, add_task, toggle_task, delete_task,
    
generate_list, get_shopping_list, clear_shopping_list
}

cl { } blocks let you embed client-side code in a server file. This is useful for the entry point:

cl {
    
import from frontend { app as ClientApp }

    
def:pub app -> JsxElement {
        
return
            
<ClientApp />;
    
}
}

Everything outside cl { } runs on the server. Everything inside runs in the browser.

Dependency-Triggered Abilities

One more concept to learn before assembling the full app. A dependency-triggered ability re-runs whenever specific state changes -- conceptually similar to React's useEffect with a dependency array, but expressed more declaratively:

    
can with [isLoggedIn] entry {
        
if isLoggedIn {
            
fetchTasks();
            
fetchShoppingList();
        
}
    
}

When isLoggedIn changes from False to True (user logs in), this ability fires automatically and loads their data. This is a powerful pattern: instead of manually calling data-loading functions after every login action, the reactive system handles it for you.

The Complete Authenticated App

Create a new project for the authenticated version:

jac
 create day-planner-auth --use client
cd day-planner-auth

You'll create these files:

day-planner-auth/
├── main.jac                # Server: nodes, AI, endpoints, entry point
├── frontend.cl.jac         # Client: state, UI, method declarations
├── frontend.impl.jac       # Client: method implementations
└── styles.css              # Styles

Run It

All the complete files are in the collapsible sections below. Create each file, then run.
Complete main.jac

Complete frontend.cl.jac

Complete frontend.impl.jac

Complete styles.css

export ANTHROPIC_API_KEY="your-key"
jac
 start main.jac

Open http://localhost:8000. You should see a login screen.

    Sign up with any username and password
    Add tasks -- they auto-categorize just like Part 5
    Try the meal planner -- type "spaghetti bolognese for 4" and click Generate
    Refresh the page -- your data persists (it's in the graph)
    Log out and sign up as a different user -- you'll see a completely empty app. Each user gets their own graph thanks to def:priv.
    Restart the server -- all data persists for both users

Visualize per-user graphs

Visit http://localhost:8000/graph to see the graph for the currently logged-in user. Log in as different users and compare -- each has their own isolated graph with their own root, tasks, and shopping items.

Step back and consider what you've built: a complete, fully functional application with authentication, per-user data isolation, AI-powered categorization, meal planning, graph persistence, and a clean multi-file architecture. In a traditional stack, this would require a web framework, an ORM, a database, an authentication library, a frontend build system, and AI integration code. In Jac, it's built with def:priv endpoints, nodes, and edges.

What You Learned

    def:priv -- private endpoints with per-user data isolation (each user gets their own root)
    jacSignup, jacLogin, jacLogout, jacIsLoggedIn -- built-in auth functions
    import from "@jac/runtime" -- import Jac's built-in client-side utilities
    can with [deps] entry -- dependency-triggered abilities (re-runs when state changes)
    cl { } -- embed client-side code in a server file
    Declaration/implementation split -- .cl.jac for UI, .impl.jac for logic
    impl app.method { ... } -- implement declared methods in a separate file

Try It Yourself

Display the logged-in username in the header next to the Sign Out button. Hint: add a currentUser: str state variable and set it from username after a successful login.
Part 7: Object-Spatial Programming with Walkers#

Your day planner is complete -- tasks persist in the graph, AI categorizes them, and you can generate shopping lists. Everything works using def:priv functions that directly manipulate graph nodes. So why learn another approach?

This final part introduces Jac's most distinctive feature: Object-Spatial Programming (OSP). It represents a fundamentally different way of thinking about code. In traditional programming, functions reach into data structures to read and modify them. In OSP, you create walkers -- mobile units of computation that travel through the graph -- and abilities -- logic that triggers automatically when a walker arrives at a node. Instead of functions that know about the entire graph, you have agents that move to data and react to what they find.

This section reimplements the day planner's backend using walkers. The app behavior stays identical -- the purpose here is purely educational: to teach you a paradigm that becomes increasingly valuable as your graphs grow deeper and more complex.

What is a Walker?

A walker is code that moves through the graph, triggering abilities as it enters each node:

spawn

visit

visit

visit

Walker: ListTasks

root

Task: "Buy groceries"

Task: "Team standup"

Task: "Go running"

ability fires

ability fires

ability fires

A helpful mental model: think of a walker like a robot moving through a building. At each room (node), it can look around (here), check its own clipboard (self), move to connected rooms (visit), and write down findings (report). The building doesn't change -- only the robot's position and what it does at each stop.

The core keywords:

    visit [-->] -- move the walker to all connected nodes
    here -- the node the walker is currently visiting
    self -- the walker itself (its own state and properties)
    report -- send data back to whoever spawned the walker
    disengage -- stop traversal immediately

Functions vs Walkers: Side by Side

The best way to understand walkers is to compare them directly with the functions you already know. Here's add_task as a def:priv function (what you built in Part 6):

def:priv add_task(title: str) -> dict {
    
category = str(categorize(title)).split(".")[-1].lower();
    
task = root ++> Task(id=str(uuid4()), title=title, category=category);
    
return {"id": task[0].id, "title": task[0].title, "done": task[0].done, "category": task[0].category};
}

And here's the same logic as a walker:

walker AddTask {
    
has title: str;

    
can create with Root entry {
        
category = str(categorize(self.title)).split(".")[-1].lower();
        
new_task = here ++> Task(
            
id=str(uuid4()),
            
title=self.title,
            
category=category
        
);
        
report {
            
"id": new_task[0].id,
            
"title": new_task[0].title,
            
"done": new_task[0].done,
            
"category": new_task[0].category
        
};
    
}
}

Study the differences carefully -- each maps directly to a concept from the function version:

    walker AddTask -- declares a walker (like a node, but mobile). Think of it as a function that goes to the data.
    has title: str -- data the walker carries with it, passed when spawning. This replaces function parameters.
    can create with Root entry -- an ability that fires when the walker enters a Root node. The with Root entry part means "execute this code when I arrive at a Root node."
    here -- the current node the walker is visiting. In the function version, you wrote root directly; in the walker version, here is whatever node the walker is currently at.
    self.title -- the walker's own properties. Since the walker is an object, its data is accessed through self.
    report { ... } -- sends data back to whoever spawned the walker. This replaces return.

Spawn it:

result = root spawn AddTask(title="Buy groceries");
print(result.reports[0]);  # The reported dict

root spawn AddTask(title="...") creates a walker and starts it at root. Whatever the walker reports ends up in result.reports.

The Accumulator Pattern

The AddTask walker may seem like unnecessary complexity compared to the function. The value of walkers becomes clearer with ListTasks, which demonstrates the accumulator pattern -- collecting data across multiple nodes as the walker traverses the graph:

walker ListTasks {
    
has results: list = [];

    
can start with Root entry {
        
visit [-->];
    
}

    
can collect with Task entry {
        
self.results.append({
            
"id": here.id,
            
"title": here.title,
            
"done": here.done,
            
"category": here.category
        
});
    
}

    
can done with Root exit {
        
report self.results;
    
}
}

Three abilities work together:

    with Root entry -- the walker enters root, visit [-->] sends it to all connected nodes
    with Task entry -- fires at each Task node, appending data to self.results
    with Root exit -- after visiting all children, the walker returns to root and reports the accumulated list

A key insight here: the walker's has results: list = [] state persists across the entire traversal. Unlike a local variable in a function call, walker state survives as the walker moves from node to node. This is what makes the accumulator pattern work -- the walker builds up its result set incrementally as it visits each node.

Compare this to the function version:

def:priv get_tasks -> list {
    
return [{"id": t.id, "title": t.title, "done": t.done, "category": t.category}
            
for t in [root-->](?:Task)];
}

For this simple, flat graph, the function version is clearly more concise. So when do walkers earn their keep? They shine when the graph is deeper. Imagine tasks containing subtasks, subtasks containing notes, and notes linking to related resources. A walker naturally recurses through the whole structure with visit [-->] at each level -- no nested loops, no recursive function calls, just "visit connected nodes" repeated at each depth.

Common issue

If walker reports come back empty, make sure you have visit [-->] to send the walker to connected nodes, and that the node type in with X entry matches your graph structure.

Node Abilities

So far, all abilities have been defined on the walker (e.g., can collect with Task entry). But Jac offers an alternative: abilities can also live on the node itself. This is an important architectural choice to understand:

node Task {
    
has id: str,
        
title: str,
        
done: bool = False,
        
category: str = "other";

    
can respond with ListTasks entry {
        
visitor.results.append({
            
"id": self.id,
            
"title": self.title,
            
"done": self.done,
            
"category": self.category
        
});
    
}
}

When a ListTasks walker visits a Task node, the node's respond ability fires automatically. Inside a node ability, visitor refers to the visiting walker (so you can access visitor.results).

Both patterns achieve the same result. The design question is: where does the logic naturally belong? Walker-side abilities make sense when the logic is about the traversal -- how to navigate, what to collect, when to stop. Node-side abilities make sense when the logic is about the data -- how a node should present itself, what it should do when visited. In practice, you'll often mix both approaches within the same application.

visit and disengage

visit [-->] queues all connected nodes for the walker to visit next. You can also filter:

visit [-->](?:Task);      # Visit only Task nodes
visit [-->] else {         # Fallback if no nodes to visit
    
report "No tasks found";
};

disengage stops the walker immediately -- this is an optimization for cases where you've found what you're looking for and don't need to visit the remaining nodes:

walker ToggleTask {
    
has task_id: str;

    
can search with Root entry { visit [-->]; }

    
can toggle with Task entry {
        
if here.id == self.task_id {
            
here.done = not here.done;
            
report {"id": here.id, "done": here.done};
            
disengage;  # Found it -- stop visiting remaining nodes
        
}
    
}
}

Without disengage, the walker would continue visiting every remaining node unnecessarily.

DeleteTask follows the same pattern:

walker DeleteTask {
    
has task_id: str;

    
can search with Root entry { visit [-->]; }

    
can remove with Task entry {
        
if here.id == self.task_id {
            
del here;
            
report {"deleted": self.task_id};
            
disengage;
        
}
    
}
}

Multi-Step Traversals

The GenerateShoppingList walker demonstrates the real power of OSP -- performing multiple operations in a single graph traversal. Read this carefully, because the execution order is subtle and important:

walker GenerateShoppingList {
    
has meal_description: str;

    
can generate with Root entry {
        
# Queue connected nodes for traversal after this ability completes
        
visit [-->];
        
# Generate new ingredients (runs before queued visits)
        
ingredients = generate_shopping_list(self.meal_description);
        
result: list = [];
        
for ing in ingredients {
            
data = {
                
"name": ing.name,
                
"quantity": ing.quantity,
                
"unit": str(ing.unit).split(".")[-1].lower(),
                
"cost": ing.cost,
                
"carby": ing.carby
            
};
            
here ++> ShoppingItem(
                
name=data["name"], quantity=data["quantity"],
                
unit=data["unit"], cost=data["cost"], carby=data["carby"]
            
);
            
result.append(data);
        
}
        
report result;
    
}

    
can clear_old with ShoppingItem entry {
        
del here;
    
}
}

Here's the key to understanding this walker: when visit [-->] runs, it doesn't immediately move the walker. Instead, it queues all connected nodes for traversal after the current ability body completes. So the rest of generate runs first -- creating new ShoppingItem nodes and building the result list. Then, once the ability body finishes, the walker traverses to the queued nodes. If any of those are ShoppingItem nodes that existed before this ability ran, the clear_old ability fires and deletes them.

Compare this to the function version, where you needed an explicit loop to clear old items before generating new ones. The walker version expresses the same intent more declaratively: "when I encounter a ShoppingItem, delete it." The cleanup logic is separated from the generation logic, making each piece easier to reason about independently.

The remaining shopping walkers follow familiar patterns:

walker GetShoppingList {
    
has items: list = [];

    
can collect with Root entry { visit [-->]; }

    
can gather with ShoppingItem entry {
        
self.items.append({
            
"name": here.name, "quantity": here.quantity,
            
"unit": here.unit, "cost": here.cost, "carby": here.carby
        
});
    
}

    
can done with Root exit { report self.items; }
}

walker ClearShoppingList {
    
can collect with Root entry { visit [-->]; }

    
can clear with ShoppingItem entry {
        
del here;
        
report {"cleared": True};
    
}
}

Spawning Walkers from the Frontend

Now that you understand how walkers work on the server, let's connect them to the frontend. In the def:priv version, the frontend called server functions directly with await add_task(title). With walkers, the frontend spawns them instead -- a different syntax but the same transparent client-server communication.

sv import brings server walkers into client code:

sv import from main {
    
AddTask, ListTasks, ToggleTask, DeleteTask,
    
GenerateShoppingList, GetShoppingList, ClearShoppingList
}

The sv prefix means "server import" -- it lets client code reference server-side walkers so it can spawn them.

Then in the frontend methods:

# Function style (Part 6):
task = await add_task(task_text.strip());

# Walker style (Part 7):
result = root spawn AddTask(title=task_text.strip());
new_task = result.reports[0];

The key pattern: root spawn Walker(params) creates a walker and starts it at root. The walker traverses the graph, and whatever it reports ends up in result.reports.

walker:priv -- Per-User Data Isolation

Just as def:priv gave functions per-user isolation, walkers can be marked with access modifiers for the same purpose:

    walker AddTask -- public, anyone can spawn it
    walker:priv AddTask -- private, requires authentication

When you use walker:priv, the walker runs on the authenticated user's own private root node. User A's tasks are completely invisible to User B -- same code, isolated data, enforced by the runtime. The complete walker version below uses :priv on all walkers, combined with the authentication you learned in Part 6.

The Complete Walker Version

Same UI, different backend

The frontend.cl.jac and styles.css files are identical to Part 6 -- only main.jac (walkers instead of def:priv functions) and frontend.impl.jac (spawning walkers instead of calling functions) change. When reading the code below, focus on those two files.

To try the walker-based version, create a new project:

jac
 create day-planner-v2 --use client
cd day-planner-v2

You'll create these files:

day-planner-v2/
├── main.jac                # Server: nodes, AI, walkers
├── frontend.cl.jac         # Client: state, UI, method declarations
├── frontend.impl.jac       # Client: method implementations
└── styles.css              # Styles

Run It

All the complete files are in the collapsible sections below. Create each file, then run.
Complete main.jac

Complete frontend.cl.jac

Complete frontend.impl.jac

Complete styles.css

export ANTHROPIC_API_KEY="your-key"
jac
 start main.jac

Open http://localhost:8000. You should see a login screen -- that's authentication working with walker:priv.

    Sign up with any username and password
    Add tasks -- they auto-categorize just like Part 5
    Try the meal planner -- type "spaghetti bolognese for 4" and click Generate
    Refresh the page -- your data persists (it's in the graph)
    Log out and sign up as a different user -- you'll see a completely empty app. Each user gets their own graph.
    Restart the server -- all data persists for both users

Visualize the graph

Visit http://localhost:8000/graph to see how walkers operate on the same graph structure as the function-based version. The nodes and edges are identical -- only the code that traverses them changed.

What You Learned

This part introduced Jac's Object-Spatial Programming paradigm:

    walker -- mobile code that traverses the graph
    can X with NodeType entry -- ability that fires when a walker enters a specific node type
    can X with NodeType exit -- ability that fires when leaving a node type
    visit [-->] -- move the walker to all connected nodes
    here -- the node the walker is currently visiting
    self -- the walker itself (its state and properties)
    visitor -- inside a node ability, the walker that's visiting
    report { ... } -- send data back, collected in .reports
    disengage -- stop traversal immediately
    root spawn Walker() -- create and start a walker at a node
    result.reports[0] -- access the walker's reported data
    walker:priv -- per-user walker with data isolation
    sv import -- import server walkers into client code

When to use each approach:
Approach 	Best For
def:pub functions 	Public endpoints, simple CRUD, quick prototyping
def:priv functions 	Per-user data isolation with private root nodes
Walkers 	Graph traversal, multi-step operations, deep/recursive graphs
walker:priv 	Per-user walker with data isolation via private root nodes
Node abilities 	When the logic naturally belongs to the data type
Walker abilities 	When the logic naturally belongs to the traversal

Try It Yourself

Write a CountTasks walker that reports the total number of tasks and how many are done, without collecting the full task list. Use self.total: int and self.completed: int counters that increment as the walker visits each Task node.
Summary#

Over seven parts, you progressed from basic syntax to a complete full-stack application, then explored an alternative programming paradigm. Here's what you accomplished:
Parts 	What You Built 	What It Teaches
1–4 	Working day planner 	Core syntax, graph data, reactive frontend
5 	+ AI features 	AI delegation, structured output, semantic types
6 	+ Auth & multi-file 	Authentication, def:priv, per-user isolation, declaration/implementation split
7 	OSP reimplementation 	Walkers, abilities, graph traversal

The concepts you've learned are interconnected. Types constrain AI output. Graphs eliminate databases. root enables per-user isolation. Walkers provide an alternative to functions for graph-heavy logic. Here's a quick reference of every Jac concept covered in this tutorial:

Data & Types: node, edge, obj, enum, has, glob, sem, type annotations, str | None unions

Graph: root, ++> (create + connect), +>: Edge :+> (typed edge), [root-->] (query), (?:Type) (filter), del (delete)

Functions: def, def:pub, def:priv, by llm(), lambda, async/await

Walkers: walker, walker:priv, can with Type entry/exit, visit, here, self, visitor, report, disengage, spawn

Frontend: cl, JsxElement, reactive has, can with entry, can with [deps] entry, JSX expressions, sv import

Structure: import from, cl import, sv import, impl, declaration/implementation split

Auth: jacSignup, jacLogin, jacLogout, jacIsLoggedIn
Next Steps#

Now that you have a solid foundation, here are some directions to deepen your understanding:

    Deploy -- Deploy to Kubernetes with jac-scale to take your app to production
    Go deeper on walkers -- Object-Spatial Programming covers advanced graph patterns like recursive traversals and multi-hop queries
    More AI -- byLLM Quickstart for standalone examples and Agentic AI for building tool-using agents
    Examples -- Explore community examples for inspiration on what to build next
    Language Reference -- Full Language Reference for complete syntax documentation when you need to look up specifics

Syntax Quick Reference#

This page is a lookup reference, not a learning guide. For hands-on learning, start with the AI Day Planner tutorial which teaches these concepts progressively.

Try it: Functions | Objects | Walkers & Graphs | AI Integration | Full Reference

# ============================================================
# Learn Jac in Y Minutes
# ============================================================
# Jac is a superset of Python with graph-native programming,
# object-spatial walkers, AI-native constructs, and full-stack
# codespaces -- all with brace-delimited blocks.
# Run a file with: jac <filename>

# ============================================================
# Comments & Docstrings
# ============================================================

# Single-line comment

#*
    Multi-line
    comment
*#

# Module-level docstring (no semicolon needed)
"""This module does something useful."""

# Docstrings go BEFORE the declaration they document
"""Object-level docstring."""
obj Documented {

    """Method docstring."""
    
def method() {
    
}
}


# ============================================================
# Entry Point
# ============================================================

# Every Jac program starts from a `with entry` block.
# You can have multiple; they run in order.

with entry {
    
print("Hello, world!");
}

# Use :__main__ to run only when this is the main module
with entry:__main__ {
    
print("Only when run directly");
}


# ============================================================
# Variables & Types
# ============================================================

with entry {
    
x: int = 42;                 # Typed variable
    
name = "Jac";                # Type inferred
    
pi: float = 3.14;
    
flag: bool = True;
    
nothing: None = None;

    
# Jac has the same built-in types as Python:
    
# int, float, str, bool, list, tuple, set, dict, bytes, any

    
# Union types
    
maybe: str | None = None;

    
# F-strings
    
msg = f"Value: {x}, Pi: {pi:.2f}";
}


# ============================================================
# Imports
# ============================================================

# Simple import
import os;
import sys, json;

# Import with alias
import datetime as dt;

# Import specific items from a module
import from math { sqrt, pi, log as logarithm }

# Relative imports
import from .sibling { helper_func }
import from ..parent.mod { SomeClass }

# Include merges a module's namespace into the current scope
include random;

# Cross-codespace imports (see Full-Stack section below)
# sv import from ...main { MyWalker }       # Server import in client
# cl import from "@jac/runtime" { Link }    # npm runtime import


# ============================================================
# Functions (def)
# ============================================================

# Functions use `def`, braces for body, and semicolons
def greet(name: str) -> str {
    
return f"Hello, {name}!";
}

# Default parameters and multiple return values
def divmod_example(a: int, b: int = 2) -> tuple[int, int] {
    
return (a // b, a % b);
}

# No-arg functions still need parentheses
def say_hi() {
    
print("Hi!");
}

# Abstract function (declaration only, no body)
def area() -> float abs;

# Function with all param types
def kitchen_sink(
    
pos_only: int,
    
/,
    
regular: str = "default",
    
*args: int,
    
kw_only: bool = True,
    
**kwargs: any
) -> str {
    
return "ok";
}

# Public function (becomes API endpoint with `jac start`)
def:pub get_items() -> list {
    
return [];
}

# Private function
def:priv internal_helper() -> None { }


# ============================================================
# Control Flow
# ============================================================

with entry {
    
x = 9;

    
# --- if / elif / else (no parens needed, braces required) ---
    
if x < 5 {
        
print("low");
    
} elif x < 10 {
        
print("medium");
    
} else {
        
print("high");
    
}

    
# --- for-in loop ---
    
for item in ["a", "b", "c"] {
        
print(item);
    
}

    
# --- for-to-by loop (C-style iteration) ---
    
# Syntax: for VAR = START to CONDITION by STEP { ... }
    
for i = 0 to i < 10 by i += 2 {
        
print(i);   # 0, 2, 4, 6, 8
    
}

    
# --- while loop (with optional else) ---
    
n = 5;
    
while n > 0 {
        
n -= 1;
    
} else {
        
print("Loop completed normally");
    
}

    
# --- break, continue, skip ---
    
for i in range(10) {
        
if i == 3 { continue; }
        
if i == 7 { break; }
        
print(i);
    
}

    
# --- ternary expression ---
    
label = "high" if x > 5 else "low";
}


# ============================================================
# Match (Python-style pattern matching)
# ============================================================

with entry {
    
value = 10;
    
match value {
        
case 1:
            
print("one");
        
case 2 | 3:
            
print("two or three");
        
case x if x > 5:
            
print(f"big: {x}");
        
case _:
            
print("other");
    
}
}


# ============================================================
# Switch (C-style, with fall-through)
# ============================================================

def check_fruit(fruit: str) {
    
switch fruit {
        
case "apple":
            
print("It's an apple");
            
break;
        
case "banana":
        
case "orange":
            
print("banana or orange (fall-through)");
        
default:
            
print("unknown fruit");
    
}
}


# ============================================================
# Collections
# ============================================================

with entry {
    
# Lists
    
fruits = ["apple", "banana", "cherry"];
    
print(fruits[0]);       # apple
    
print(fruits[1:3]);     # ["banana", "cherry"]
    
print(fruits[-1]);      # cherry

    
# Dictionaries
    
person = {"name": "Alice", "age": 25};
    
print(person["name"]);

    
# Tuples (immutable)
    
point = (10, 20);
    
(x, y) = point;         # Tuple unpacking

    
# Sets
    
colors = {"red", "green", "blue"};

    
# Comprehensions
    
squares = [i ** 2 for i in range(5)];
    
evens = [i for i in range(10) if i % 2 == 0];
    
name_map = {name: len(name) for name in ["alice", "bob"]};
    
unique_lens = {len(s) for s in ["hi", "hey", "hi"]};

    
# Generator expression
    
total = sum(x ** 2 for x in range(1000));

    
# Star unpacking
    
(first, *rest) = [1, 2, 3, 4];
    
print(first);   # 1
    
print(rest);    # [2, 3, 4]
}


# ============================================================
# Objects (obj) vs Classes (class)
# ============================================================

# `obj` is like a Python dataclass -- fields are per-instance,
# auto-generates __init__, __eq__, __repr__, etc.
obj Dog {
    
has name: str = "Unnamed",
        
age: int = 0;

    
def bark() {
        
print(f"{self.name} says Woof!");
    
}
}

# `class` follows standard Python class behavior
class Cat {
    
has name: str = "Unnamed";

    
def meow(self) {
        
print(f"{self.name} says Meow!");
    
}
}

# Inheritance
obj Puppy(Dog) {
    
has parent_name: str = "Unknown";

    
override def bark() {
        
print(f"Puppy of {self.parent_name} yips!");
    
}
}

# Generic types with type parameters
obj Result[T, E = Exception] {
    
has value: T | None = None,
        
error: E | None = None;

    
def is_ok() -> bool {
        
return self.error is None;
    
}
}

# Forward declaration (define body later or in another file)
obj UserProfile;


# ============================================================
# Has Declarations (fields)
# ============================================================

obj Example {
    
# Basic typed fields with defaults
    
has name: str,
        
count: int = 0;

    
# Static (class-level) field
    
static has instances: int = 0;

    
# Deferred initialization (set in postinit)
    
has computed: int by postinit;

    
def postinit() {
        
self.computed = self.count * 2;
    
}
}


# ============================================================
# Access Modifiers
# ============================================================

# Access modifiers work on obj, class, node, edge, walker,
# def, has -- controlling visibility and API exposure

obj:pub Person {
    
has:pub name: str;          # Public (default)
    
has:priv ssn: str;          # Private
    
has:protect age: int;       # Protected
}

# Public walker becomes REST endpoint with `jac start`
walker:pub GetUsers {
    
can get with Root entry {
        
report [-->];
    
}
}

# Private walker enforces per-user auth
walker:priv MyData {
    
can get with Root entry {
        
report [-->];
    
}
}


# ============================================================
# Enums
# ============================================================

enum Color {
    
RED = "red",
    
GREEN = "green",
    
BLUE = "blue"
}

# Auto-valued enum members
enum Status { PENDING, ACTIVE, DONE }

with entry {
    
print(Color.RED.value);      # "red"
    
print(Status.ACTIVE.value);  # 2
}


# ============================================================
# Type Aliases
# ============================================================

type JsonPrimitive = str | int | float | bool | None;
type Json = JsonPrimitive | list[Json] | dict[str, Json];

# Generic type alias
type NumberList = list[int | float];


# ============================================================
# Global Variables (glob)
# ============================================================

glob MAX_SIZE: int = 100;
glob greeting: str = "Hello";

def use_global() {
    
global greeting;          # Reference module-level glob
    
greeting = "Hola";
}


# ============================================================
# Impl Blocks (separate declaration from definition)
# ============================================================

obj Calculator {
    
has value: int = 0;

    
# Declare methods (no body)
    
def add(n: int) -> int;
    
def multiply(n: int) -> int;
}

# Define methods separately (can be in a .impl.jac file)
impl Calculator.add(n: int) -> int {
    
self.value += n;
    
return self.value;
}

impl Calculator.multiply(n: int) -> int {
    
self.value *= n;
    
return self.value;
}


# ============================================================
# Lambdas
# ============================================================

with entry {
    
# Simple lambda (untyped params, colon body)
    
add = lambda x, y: x + y;
    
print(add(3, 4));

    
# Typed lambda with return type
    
mul = lambda (x: int, y: int) -> int : x * y;
    
print(mul(3, 4));

    
# Multi-statement lambda (brace body)
    
classify = lambda (score: int) -> str {
        
if score >= 90 { return "A"; }
        
elif score >= 80 { return "B"; }
        
else { return "F"; }
    
};
    
print(classify(85));

    
# No-arg lambda
    
get_42 = lambda : 42;

    
# Void lambda (common in JSX event handlers)
    
handler = lambda -> None { print("clicked"); };
}


# ============================================================
# Pipe Operators
# ============================================================

with entry {
    
# Forward pipe: value |> function
    
"hello" |> print;
    
5 |> str |> print;

    
# Backward pipe: function <| value
    
print <| "world";

    
# Chained pipes
    
[3, 1, 2] |> sorted |> list |> print;
}


# ============================================================
# Decorators
# ============================================================

@classmethod
def my_class_method(cls: type) -> str {
    
return cls.__name__;
}


# ============================================================
# Try / Except / Finally
# ============================================================

with entry {
    
try {
        
result = 10 // 0;
    
} except ZeroDivisionError as e {
        
print(f"Caught: {e}");
    
} except Exception {
        
print("Some other error");
    
} else {
        
print("No error occurred");
    
} finally {
        
print("Always runs");
    
}
}


# ============================================================
# With Statement (context managers)
# ============================================================

with entry {
    
with open("file.txt") as f {
        
data = f.read();
    
}

    
# Multiple context managers
    
with open("a.txt") as a, open("b.txt") as b {
        
print(a.read(), b.read());
    
}
}


# ============================================================
# Assert
# ============================================================

with entry {
    
x = 42;
    
assert x == 42;
    
assert x > 0, "x must be positive";
}


# ============================================================
# Walrus Operator (:=)
# ============================================================

with entry {
    
# Assignment inside expressions
    
if (n := len("hello")) > 3 {
        
print(f"Long string: {n} chars");
    
}
}


# ============================================================
# Test Blocks
# ============================================================

def fib(n: int) -> int {
    
if n <= 1 { return n; }
    
return fib(n - 1) + fib(n - 2);
}

test "fibonacci base cases" {
    
assert fib(0) == 0;
    
assert fib(1) == 1;
}

test "fibonacci recursive" {
    
for i in range(2, 10) {
        
assert fib(i) == fib(i - 1) + fib(i - 2);
    
}
}

# Tests can spawn walkers and check reports
test "walker test" {
    
root ++> Person(name="Alice", age=30);
    
result = root spawn Greeter();
    
assert len(result.reports) > 0;
}


# ============================================================
# Async / Await
# ============================================================

import asyncio;

async def fetch_data() -> str {
    
await asyncio.sleep(1);
    
return "data";
}

async def main() {
    
result = await fetch_data();
    
print(result);
}


# ============================================================
# Flow / Wait (concurrent tasks)
# ============================================================

import from time { sleep }

def slow_task(n: int) -> int {
    
sleep(1);
    
return n * 2;
}

with entry {
    
# `flow` launches a concurrent task, `wait` collects results
    
task1 = flow slow_task(1);
    
task2 = flow slow_task(2);
    
task3 = flow slow_task(3);

    
r1 = wait task1;
    
r2 = wait task2;
    
r3 = wait task3;
    
print(r1, r2, r3);   # 2 4 6
}


# ============================================================
# Null-Safe Access (?. and ?[])
# ============================================================

with entry {
    
x: list | None = None;
    
print(x?.append);      # None (no crash)
    
print(x?[0]);           # None (no crash)

    
y = [1, 2, 3];
    
print(y?[1]);           # 2
    
print(y?[99]);          # None (out of bounds returns None)
}


# ============================================================
# Inline Python (::py::)
# ============================================================

with entry {
    
result: int = 0;
    
::py::
import sys
result = sys.maxsize
    
::py::
    
print(f"Max int: {result}");
}

# Also works inside objects/enums for Python-specific methods
enum Priority {
    
LOW = 1,
    
HIGH = 2

    
::py::
    
def is_urgent(self):
        
return self.value >= 2
    
::py::
}


# ============================================================
# OBJECT SPATIAL PROGRAMMING (OSP)
# ============================================================
# Jac extends the type system with graph-native constructs:
# nodes, edges, walkers, and spatial abilities.


# ============================================================
# Nodes and Edges
# ============================================================

# Nodes are objects that can exist in a graph
node Person {
    
has name: str,
        
age: int;
}

# Edges connect nodes and can carry data
edge Friendship {
    
has since: int = 0;
}

# Nodes with abilities (triggered by walkers)
node SecureRoom {
    
has name: str,
        
clearance: int = 0;

    
can on_enter with Visitor entry {
        
print(f"Welcome to {self.name}");
    
}

    
can on_exit with Visitor exit {
        
print(f"Leaving {self.name}");
    
}
}

# Node inheritance
node Employee(Person) {
    
has department: str;
}

# Edge with methods
edge Weighted {
    
has weight: float = 1.0;

    
def normalize(max_w: float) -> float {
        
return self.weight / max_w;
    
}
}


# ============================================================
# Connection Operators
# ============================================================

with entry {
    
a = Person(name="Alice", age=25);
    
b = Person(name="Bob", age=30);
    
c = Person(name="Charlie", age=28);

    
# --- Untyped connections ---
    
root ++> a;             # Connect root -> a
    
a ++> b;                # Connect a -> b
    
c <++ a;                # Connect a -> c (backward syntax)
    
a <++> b;               # Bidirectional a <-> b

    
# --- Typed connections (with edge data) ---
    
a +>: Friendship(since=2020) :+> b;
    
a +>: Friendship(since=1995) :+> c;

    
# --- Typed connection with field assignment ---
    
a +>: Friendship : since=2018 :+> b;

    
# --- Chained connections ---
    
root ++> a ++> b ++> c;

    
# --- Delete edge ---
    
a del --> b;

    
# --- Delete node ---
    
del c;
}


# ============================================================
# Edge Traversal & Filters
# ============================================================

with entry {
    
# Traverse outgoing edges from root
    
print([root -->]);                      # All nodes via outgoing edges
    
print([root <--]);                      # All nodes via incoming edges
    
print([root <-->]);                     # All nodes via any edges

    
# Filter by edge type
    
print([root ->:Friendship:->]);          # Nodes connected by Friendship edges

    
# Filter by edge field values
    
print([root ->:Friendship:since > 2018:->]);

    
# Filter by node type
    
print([root -->](?:Person));             # Only Person nodes

    
# Filter by node attribute
    
print([root -->](?age >= 18));           # Nodes with age >= 18

    
# Combined: type + attribute
    
print([root -->](?:Person, age > 25));

    
# Get edge objects themselves (not target nodes)
    
print([edge root -->]);                  # All edge objects
    
print([edge root ->:Friendship:->]);     # Friendship edge objects

    
# Chained traversal (multi-hop)
    
fof = [root ->:Friendship:-> ->:Friendship:->];
}


# ============================================================
# Assign Comprehensions (spatial update)
# ============================================================

with entry {
    
# Filter nodes by attribute
    
adults = [root -->](?age >= 18);

    
# Assign: update matching nodes in-place
    
[root -->](?age >= 18)(=verified=True);
}


# ============================================================
# Walkers
# ============================================================
# Walkers are objects that traverse graphs.
# They have abilities that trigger on entry/exit of nodes.

walker Greeter {
    
has greeting: str = "Hello";

    
# Runs when walker enters the root node
    
can greet_root with Root entry {
        
print(f"{self.greeting} from root!");
        
visit [-->];        # Move to connected nodes
    
}

    
# Runs when walker visits any Person node
    
can greet_person with Person entry {
        
# `here` = current node, `self` = the walker
        
print(f"{self.greeting}, {here.name}!");
        
report here.name;   # Collect a value (returned as list)
        
visit [-->];         # Continue traversal
    
}
}

with entry {
    
root ++> Person(name="Alice", age=25);
    
root ++> Person(name="Bob", age=30);

    
# Spawn a walker at root and collect results
    
result = root spawn Greeter();
    
print(result.reports);   # ["Alice", "Bob"]
}


# ============================================================
# Walker Control Flow
# ============================================================

walker SearchWalker {
    
has target: str;

    
can search with Person entry {
        
if here.name == self.target {
            
print(f"Found {self.target}!");
            
disengage;       # Stop traversal immediately
        
}
        
report here.name;

        
# visit...else runs fallback when no outgoing nodes
        
visit [-->] else {
            
print("Reached a dead end");
        
}
    
}
}


# ============================================================
# Visit Statement Variants
# ============================================================

walker VisitDemo {
    
can demo with Person entry {
        
visit [-->];                    # All outgoing nodes
        
visit [<--];                    # All incoming nodes
        
visit [<-->];                   # Both directions
        
visit [-->](?:Person);          # Type-filtered
        
visit [->:Friendship:->];       # Via edge type
        
visit [->:Friendship:since > 2020:->];  # Edge condition

        
visit [-->] else {              # Fallback if nowhere to go
            
print("Dead end");
        
}

        
visit : 0 : [-->];             # First outgoing node only
        
visit : -1 : [-->];            # Last outgoing node only

        
visit here;                     # Re-visit current node
    
}
}


# ============================================================
# Node & Edge Abilities
# ============================================================
# Nodes and edges can have abilities that trigger
# when specific walker types visit them.

node Gateway {
    
has name: str;

    
# Triggers for any walker
    
can on_any with entry {
        
print(f"Someone entered {self.name}");
    
}

    
# Triggers only for specific walker type
    
can on_inspector with Inspector entry {
        
if visitor.clearance < 5 {
            
print("Access denied");
            
disengage;
        
}
    
}

    
# Multiple walker types (union)
    
can on_multi with Admin | Inspector entry {
        
print("Authorized personnel");
    
}

    
# Exit ability
    
can on_leave with Inspector exit {
        
print("Inspector leaving");
    
}
}

walker Inspector {
    
has clearance: int = 0;

    
can visit_gateway with Gateway entry {
        
# `here` = current Gateway node
        
# `self` = the walker
        
print(f"Inspecting: {here.name}");
        
visit [-->];
    
}
}


# ============================================================
# Typed Context Blocks
# ============================================================
# Handle different subtypes with specialized code paths

node Animal { has name: str; }
node Dog(Animal) { has breed: str; }
node Cat(Animal) { has indoor: bool; }

walker AnimalVisitor {
    
can visit_animal with Animal entry {
        
->Dog{print(f"{here.name} is a {here.breed} dog");}
        
->Cat{print(f"{here.name} says meow");}
        
->_{print(f"{here.name} is some animal");}
    
}
}


# ============================================================
# Spawn Syntax Variants
# ============================================================

with entry {
    
w = Greeter(greeting="Hi");

    
# Binary spawn: node spawn walker
    
root spawn w;

    
# Spawn with params
    
root spawn Greeter(greeting="Hey");

    
# Spawn returns result object
    
result = root spawn Greeter();
    
print(result.reports);   # List of reported values

    
# Reverse: walker spawn node
    
w spawn root;
}


# ============================================================
# Walkers as REST APIs
# ============================================================
# Public walkers become HTTP endpoints with `jac start`

walker:pub add_todo {
    
has title: str;          # Becomes request body field

    
can create with Root entry {
        
new_todo = here ++> Todo(title=self.title);
        
report new_todo;     # Becomes response body
    
}
}

# Endpoint: POST /walker/add_todo
# Body: {"title": "Learn Jac"}

# Public functions also become endpoints
def:pub health_check() -> dict {
    
return {"status": "ok"};
}

# @restspec customizes HTTP method and path
import from http { HTTPMethod }

@restspec(method=HTTPMethod.GET, path="/items/{item_id}")
walker:pub get_item {
    
has item_id: str;
    
can fetch with Root entry {
        
report {"id": self.item_id};
    
}
}


# ============================================================
# Async Walkers
# ============================================================

async walker AsyncCrawler {
    
has depth: int = 0;

    
async can crawl with Root entry {
        
print(f"Crawling at depth {self.depth}");
        
visit [-->];
    
}
}


# ============================================================
# Anonymous Abilities
# ============================================================
# Abilities without names (auto-named by compiler)

node AutoNode {
    
has val: int = 0;

    
can with entry {
        
print(f"Entered node with val={self.val}");
    
}
}

walker AutoWalker {
    
can with Root entry {
        
visit [-->];
    
}

    
can with AutoNode entry {
        
print(f"Visiting: {here.val}");
    
}
}


# ============================================================
# Graph Built-in Functions
# ============================================================

with entry {
    
p = Person(name="Alice", age=30);
    
root ++> p;

    
jid(p);              # Unique Jac ID of object
    
save(p);             # Persist node to storage
    
commit();            # Commit pending changes
    
printgraph(root);    # Print graph for debugging
}


# ============================================================
# AI INTEGRATION (by llm)
# ============================================================
# Jac's Meaning Typed Programming lets the compiler
# extract semantics from your code to construct LLM prompts.


# ============================================================
# by llm() -- Delegate Function to LLM
# ============================================================

# The function signature IS the specification.
# Name, param names, types, and return type become the prompt.

def classify_sentiment(text: str) -> str by llm;

# Enums constrain LLM output to valid values
enum Category { WORK, PERSONAL, SHOPPING, HEALTH, OTHER }
def categorize(title: str) -> Category by llm();

# Structured output -- every field must be filled
obj Ingredient {
    
has name: str,
        
cost: float,
        
carby: bool;
}
def plan_shopping(recipe: str) -> list[Ingredient] by llm();

# Model configuration
def summarize(text: str) -> str by llm(
    
model_name="gpt-4",
    
temperature=0.7,
    
max_tokens=2000
);

# Streaming response (returns generator)
def stream_story(prompt: str) -> str by llm(stream=True);

# Inline LLM expression
with entry {
    
result = "Explain quantum computing simply" by llm;
}


# ============================================================
# sem -- Semantic Descriptions for AI
# ============================================================
# `sem` attaches descriptions to bindings that the compiler
# includes in the LLM prompt. It's not a comment -- it
# changes what the LLM sees at runtime.

sem Ingredient.cost = "Estimated cost in USD";
sem Ingredient.carby = "True if high in carbohydrates";

sem plan_shopping = "Generate a shopping list for the given recipe.";

# Parameter-level semantics
sem summarize.text = "The article or document to summarize";
sem summarize.return = "A 2-3 sentence summary";

# Enum value semantics
enum Priority { LOW, MEDIUM, HIGH, CRITICAL }
sem Priority.CRITICAL = "Requires immediate attention within 1 hour";


# ============================================================
# Tool Calling (Agentic AI)
# ============================================================
# Give the LLM access to functions it can call (ReAct loop)

def get_weather(city: str) -> str {
    
return f"Weather data for {city}";
}

def search_web(query: str) -> list[str] {
    
return [f"Result for {query}"];
}

# The LLM decides which tools to call and in what order
def answer_question(question: str) -> str by llm(
    
tools=[get_weather, search_web]
);

# Additional context injection
glob company_info = "TechCorp, products: CloudDB, SecureAuth";

def support_agent(question: str) -> str by llm(
    
incl_info={"company": company_info}
);
sem support_agent = "Answer customer questions about our products.";


# ============================================================
# Multimodal AI
# ============================================================

import from byllm.lib { Image }

def describe_image(image: Image) -> str by llm;

with entry {
    
desc = describe_image(Image("photo.jpg"));
    
desc = describe_image(Image("https://example.com/img.png"));
}


# ============================================================
# FULL-STACK DEVELOPMENT (Codespaces)
# ============================================================
# Jac code can target different execution environments:
#   sv { } = server (Python/PyPI)
#   cl { } = client (JavaScript/npm)
#   na { } = native (C ABI)


# ============================================================
# Codespace Blocks
# ============================================================

# Server code (default -- code outside any block is server)
node Todo {
    
has title: str, done: bool = False;
}

def:pub get_todos() -> list {
    
return [{"title": t.title} for t in [root -->](?:Todo)];
}

# Client code (compiles to JavaScript/React)
cl {
    
def:pub app() -> JsxElement {
        
has items: list = [];

        
async can with entry {
            
items = await get_todos();
        
}

        
return <div>
            {[<p key={i.title}>{i.title}</p> for i in items]}
        
</div>;
    
}
}

# Explicit server block
sv {
    
node Secret { has value: str; }
}

# Single-statement form (no braces)
sv import from .database { connect_db }
cl import from react { useState }


# ============================================================
# File Extension Conventions
# ============================================================
# .jac           Default (server codespace)
# .sv.jac        Server-only variant
# .cl.jac        Client-only variant (auto client codespace)
# .na.jac        Native variant
# .impl.jac      Implementation annex (method bodies)
# .test.jac      Test annex


# ============================================================
# Client Components (JSX)
# ============================================================

cl {
    
def:pub Counter() -> JsxElement {
        
# `has` in client components becomes React useState
        
has count: int = 0;

        
return <div>
            <p>Count: {count}</p>
            <button onClick={lambda -> None { count = count + 1; }}>
                Increment
            </button>
        </div>;
    
}
}

# JSX syntax reference:
# <div>text</div>               HTML elements
# <Component prop="val" />      Component with props
# {expression}                  JavaScript expression
# {condition and <p>Show</p>}   Conditional render
# {[<li>...</li> for x in xs]}  List rendering
# <div {...props}>               Spread props
# <div className="cls">         Class name (not "class")
# <div style={{"color": "red"}} Inline styles


# ============================================================
# Client State & Lifecycle
# ============================================================

cl {
    
def:pub DataView() -> JsxElement {
        
has data: list = [];
        
has loading: bool = True;

        
# Mount effect (runs once on component mount)
        
async can with entry {
            
data = await fetch("/api/data").then(
                
lambda r: any -> any { return r.json(); }
            
);
            
loading = False;
        
}

        
# Dependency effect (runs when userId changes)
        
# async can with [userId] entry { ... }

        
# Multiple dependencies
        
# can with (a, b) entry { ... }

        
# Cleanup on unmount
        
# can with exit { unsubscribe(); }

        
if loading { return <p>Loading...</p>; }
        
return <div>{data}</div>;
    
}
}


# ============================================================
# Server-Client Communication
# ============================================================

# Import server walkers in client code
sv import from ...main { AddTodo, GetTodos }

cl {
    
def:pub TodoApp() -> JsxElement {
        
has todos: list = [];

        
async can with entry {
            
result = root spawn GetTodos();
            
if result.reports {
                
todos = result.reports[0];
            
}
        
}

        
async def add_todo(text: str) -> None {
            
result = root spawn AddTodo(title=text);
            
if result.reports {
                
todos = todos + [result.reports[0]];
            
}
        
}

        
return <div>...</div>;
    
}
}


# ============================================================
# Routing (File-Based)
# ============================================================
# pages/index.jac          -> /
# pages/about.jac          -> /about
# pages/users/[id].jac     -> /users/:id  (dynamic param)
# pages/[...notFound].jac  -> *            (catch-all)
# pages/(auth)/layout.jac  -> route group  (no URL segment)
# pages/layout.jac         -> root layout

# Page files export a `page` function:
# cl { def:pub page() -> JsxElement { ... } }

# Layout files use <Outlet /> for child routes:
# cl import from "@jac/runtime" { Outlet }
# cl { def:pub layout() -> JsxElement {
#     return <><nav>...</nav><Outlet /></>;
# } }


# ============================================================
# Authentication (Client)
# ============================================================

# cl import from "@jac/runtime" {
#     jacLogin,       # (email, pass) -> bool
#     jacSignup,      # (email, pass) -> dict
#     jacLogout,      # () -> void
#     jacIsLoggedIn   # () -> bool
# }


# ============================================================
# Special Variables Reference
# ============================================================
# self     -- the current object/walker/node
# here     -- the current node (in walker abilities)
# visitor  -- the visiting walker (in node/edge abilities)
# root     -- the root node of the graph


# ============================================================
# Keywords Reference
# ============================================================
# Types:    str, int, float, bool, list, tuple, set, dict, bytes, any, type
# Decl:     obj, class, node, edge, walker, enum, has, can, def, impl,
#           glob, test, type
# Modifiers: pub, priv, protect, static, override, abs, async
# Control:  if, elif, else, for, to, by, while, match, switch, case, default
# Flow:     return, yield, break, continue, raise, del, assert, skip
# OSP:      visit, spawn, entry, exit, disengage, report, here, visitor, root
# AI:       by, llm, sem
# Async:    async, await, flow, wait
# Logic:    and, or, not, in, is
# Codespace: sv, cl, na
# Other:    import, include, from, as, try, except, finally, with, lambda,
#           global, nonlocal, self, super, init, postinit

Jac vs Traditional Stack: A Side-by-Side Comparison#

This document compares building the same Todo application using Jac versus a traditional Python + FastAPI + SQLite + TypeScript + React stack.
Jac Implementation#

# This single jac program is a fullstack application
node Todo {
    
has title: str,
        
done: bool;
}

def:pub get_todos -> list {
    
root ++> [
        
Todo("build startup", False),
        
Todo("raise funding", False),
        
Todo("change the world", False)
    
];
    
return [{"title": t.title, "done": t.done} for t in [root-->](?:Todo)];
}

cl def:pub app() -> JsxElement {
    
has items: list = [];

    
async can with entry {
        
items = await get_todos();
    
}

    
return
        
<div>
            {[<div key={item.title}>
                <input type="checkbox" checked={item.done} />
                {item.title}
            </div> for item in items]}
        
</div>;
}

What this file provides:

    node Todo defines the data model with automatic persistence to a graph database
    def:pub get_todos creates an HTTP API endpoint
    cl def:pub app() defines a React component that runs on the client
    has items becomes useState in the generated JavaScript
    async can with entry becomes useEffect(() => {...}, []) for loading data on mount
    with entry seeds initial data into the graph database
    await get_todos() handles the HTTP request to the backend

Traditional Stack Implementation#

The equivalent functionality using Python, FastAPI, SQLite, TypeScript, and React.
Backend#
backend/requirements.txt#

fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3

Purpose: Lists Python package dependencies. Python's package manager (pip) uses this file to install FastAPI (web framework), Uvicorn (ASGI server), SQLAlchemy (database ORM), and Pydantic (data validation).
backend/database.py#

"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    
SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    
db = SessionLocal()
    
try:
        
yield db
    
finally:
        
db.close()

Purpose: Configures the SQLite database connection, creates the SQLAlchemy engine, sets up session management, and provides a dependency function for database access in API endpoints.
backend/models.py#

"""SQLAlchemy models and Pydantic schemas."""
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from database import Base


class TodoModel(Base):
    """SQLAlchemy model for Todo items."""
    
__tablename__ = "todos"

    
id = Column(Integer, primary_key=True, index=True)
    
title = Column(String, nullable=False)
    
done = Column(Boolean, default=False)


class TodoResponse(BaseModel):
    """Pydantic schema for Todo response."""
    
title: str
    
done: bool

    
class Config:
        
from_attributes = True

Purpose: Defines the data structure twice: once as a SQLAlchemy model for database operations, and once as a Pydantic schema for API response serialization.
backend/main.py#

"""FastAPI Todo Application - Backend API."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import TodoModel, TodoResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    
Base.metadata.create_all(bind=engine)
    
db = next(get_db())
    
if db.query(TodoModel).count() == 0:
        
initial_todos = [
            
TodoModel(title="build startup", done=False),
            
TodoModel(title="raise funding", done=False),
            
TodoModel(title="change the world", done=False),
        
]
        
db.add_all(initial_todos)
        
db.commit()
    
db.close()
    
yield


app = FastAPI(title="Todo API", lifespan=lifespan)

app.add_middleware(
    
CORSMiddleware,
    
allow_origins=["http://localhost:5173"],
    
allow_credentials=True,
    
allow_methods=["*"],
    
allow_headers=["*"],
)


@app.get("/api/todos", response_model=list[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    """Get all todos."""
    
return db.query(TodoModel).all()


if __name__ == "__main__":
    
import uvicorn
    
uvicorn.run(app, host="0.0.0.0", port=8000)

Purpose: Creates the FastAPI application, configures CORS middleware for frontend access, defines the API endpoint, handles database initialization on startup, and seeds initial data.
Frontend#
frontend/package.json#

{
  "name": "todo-app-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.12"
  }
}

Purpose: Node.js package manifest that lists JavaScript/TypeScript dependencies (React, TypeScript, Vite) and defines npm scripts for development and building.
frontend/tsconfig.json#

{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}

Purpose: Configures the TypeScript compiler with target JavaScript version, module resolution strategy, JSX handling, and type-checking rules.
frontend/tsconfig.node.json#

{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}

Purpose: Separate TypeScript configuration for Node.js-executed files like vite.config.ts, which run in a different environment than browser code.
frontend/vite.config.ts#

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})

Purpose: Configures Vite build tool with React plugin support and sets up a development proxy to forward /api requests to the backend server.
frontend/index.html#

<!DOCTYPE html>
<html lang="en">
  
<head>
    
<meta charset="UTF-8" />
    
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
<title>Todo App</title>
  
</head>
  
<body>
    
<div id="root"></div>
    
<script type="module" src="/src/main.tsx"></script>
  
</body>
</html>

Purpose: HTML entry point that provides the root DOM element where React mounts and loads the TypeScript entry point.
frontend/src/types.ts#

export interface Todo {
  title: string;
  done: boolean;
}

Purpose: TypeScript interface definitions for data structures. These must be kept in sync with the backend Pydantic schemas.
frontend/src/api.ts#

import { Todo } from './types';

export async function getTodos(): Promise<Todo[]> {
  const response = await fetch('/api/todos');
  if (!response.ok) {
    throw new Error('Failed to fetch todos');
  }
  return response.json();
}

Purpose: API client function that wraps the fetch call to communicate with the backend, handling HTTP requests and error checking.
frontend/src/App.tsx#

import { useState, useEffect } from 'react';
import { Todo } from './types';
import { getTodos } from './api';

export default function App() {
  const [items, setItems] = useState<Todo[]>([]);

  useEffect(() => {
    async function loadTodos() {
      const todos = await getTodos();
      setItems(todos);
    }
    loadTodos();
  }, []);

  return (
    <div>
      {items.map((item) => (
        <div key={item.title}>
          <input type="checkbox" checked={item.done} readOnly />
          {item.title}
        </div>
      ))}
    </div>
  );
}

Purpose: Main React component that manages state with useState, loads data on mount with useEffect, and renders the todo list.
frontend/src/main.tsx#

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

Purpose: React application entry point that mounts the App component into the DOM root element.
What Each Approach Requires#
Component 	Traditional Stack 	Jac
Database configuration 	Explicit setup 	Automatic
ORM model 	Required 	node declaration
API serialization schema 	Required (Pydantic) 	Automatic
API route definition 	Required (decorator) 	def:pub
CORS configuration 	Required 	Automatic
Frontend type definitions 	Required 	Shared with backend
API client code 	Required 	Automatic RPC
React state setup 	useState hook 	has declaration
Data loading effect 	useEffect hook 	can with entry
Build tooling config 	Required (Vite, TS) 	Automatic
HTML entry point 	Required 	Automatic

MCP Server (jac-mcp)#

The jac-mcp plugin provides a Model Context Protocol server that gives AI assistants deep knowledge of the Jac language. It exposes grammar specifications, documentation, code examples, compiler tools, and prompt templates through a standardized protocol.
Installation#

pip
 install jac-mcp

Or for development:

pip
 install -e ./jac-mcp

Quick Start#
Start the MCP server (stdio transport)#

jac
 mcp

Start with SSE transport#

jac
 mcp --transport sse --port 3001

Inspect available resources, tools, and prompts#

jac
 mcp --inspect

Configuration#

Add to your project's jac.toml:

[plugins.mcp]
transport = "stdio"
port = 3001
host = "127.0.0.1"
expose_grammar = true
enable_validate = true

Resources (24+)#

Resources are read-only reference materials that AI models can load for context.
URI Pattern 	Description
jac://grammar/spec 	Full EBNF grammar specification
jac://grammar/tokens 	Token and keyword definitions
jac://docs/foundation 	Core language concepts
jac://docs/functions-objects 	Archetypes, abilities, has declarations
jac://docs/osp 	Object-Spatial Programming (nodes, edges, walkers)
jac://docs/primitives 	Primitives and codespace semantics
jac://docs/concurrency 	Concurrency (flow, wait, async)
jac://docs/advanced 	Comprehensions and filters
jac://docs/cheatsheet 	Quick syntax reference
jac://docs/python-integration 	Python interoperability
jac://docs/byllm 	byLLM plugin reference
jac://docs/jac-client 	jac-client plugin reference
jac://docs/jac-scale 	jac-scale plugin reference
jac://guide/pitfalls 	Common AI mistakes when writing Jac
jac://guide/patterns 	Idiomatic Jac code patterns
jac://examples/* 	Example Jac projects
Tools (9)#

Tools are executable operations that AI models can invoke.
Tool 	Description
validate_jac 	Full type-check validation of Jac code
check_syntax 	Quick parse-only syntax check
format_jac 	Format Jac code to standard style
py_to_jac 	Convert Python code to Jac
explain_error 	Explain compiler errors with suggestions
list_examples 	List available example categories
get_example 	Get example code files
search_docs 	Keyword search across documentation
get_ast 	Parse code and return AST info
Prompts (9)#

Prompt templates for common Jac development tasks.
Prompt 	Description
write_module 	Generate a new Jac module
write_impl 	Generate .impl.jac implementation file
write_walker 	Generate a walker with visit logic
write_node 	Generate a node archetype
write_test 	Generate test blocks
write_ability 	Generate an ability implementation
debug_error 	Debug a compilation error
fix_type_error 	Fix a type checking error
migrate_python 	Convert Python to idiomatic Jac
IDE Integration#
Claude Desktop#

Add to your Claude Desktop config (~/.claude/claude_desktop_config.json):

{
  "mcpServers": {
    "jac": {
      "command": "jac",
      "args": ["mcp"]
    }
  }
}

VS Code with Continue#

Add to your Continue config:

{
  "mcpServers": [
    {
      "name": "jac",
      "command": "jac",
      "args": ["mcp"]
    }
  ]
}

Transport Options#
Transport 	Flag 	Description
stdio 	--transport stdio 	Default. Standard input/output. Best for IDE integration.
SSE 	--transport sse 	Server-Sent Events over HTTP. Requires uvicorn and starlette.
Streamable HTTP 	--transport streamable-http 	HTTP streaming. Requires uvicorn and starlette.


Reference#

This section is the complete technical reference for Jac. Use the sidebar to navigate to the topic you need, or use the summaries below to find the right starting point.
Language Specification#

The language spec covers all core Jac constructs:

    Foundation - Syntax, types, literals, variables, scoping, operators, control flow, pattern matching
    Functions & Objects - Function declarations, can vs def, OOP, inheritance, enums, access modifiers, impl blocks
    Object-Spatial Programming - Nodes, edges, walkers, visit, report, disengage, graph construction, data spatial queries, common patterns
    Concurrency - Async/await, flow/wait concurrent expressions, parallel operations
    Comprehensions & Filters - Filter/assign comprehensions, typed filters

AI Integration#

    byLLM Reference - by llm(), model configuration, tool calling, streaming, multimodal input, agentic patterns

Full-Stack Development#

    jac-client Reference - Codespaces, components, state, routing, authentication, npm packages

Deployment & Scaling#

    jac-scale Reference - Production deployment, API generation, Kubernetes, monitoring

Tools & Config#

    CLI Commands - Every jac subcommand with options and examples
    Configuration - Project settings via jac.toml
    Testing - Test syntax, assertions, and CLI test commands

Python Integration#

    Interoperability - Importing and using Python packages in Jac, five adoption patterns
    Library Mode - Using Jac features from pure Python code

Quick Reference#

    Walker Patterns - The .reports array, response patterns, nested walker spawning
    Appendices - Complete keyword reference, operator quick reference, grammar, gotchas, migration guide

Quick Start#

# 1. Install
pip
 install jaseci

# 2. Scaffold a new project
jac
 create myapp --use client

# 3. Run
jac
 start main.jac

CLI Quick Reference#

The jac command is your primary interface to the Jac toolchain. For the full reference, see CLI Commands.
Execution Commands#
Command 	Description
jac run <file> 	Execute Jac program
jac enter <file> <entry> 	Run named entry point
jac start [file] 	Start web server
jac debug <file> 	Run in debug mode
Analysis Commands#
Command 	Description
jac check 	Type check code
jac format 	Format source files
jac test 	Run test suite
Transform Commands#
Command 	Description
jac py2jac <file> 	Convert Python to Jac
jac jac2py <file> 	Convert Jac to Python
jac js <file> 	Compile to JavaScript
Project Commands#
Command 	Description
jac create 	Create new project
jac install 	Install all dependencies (pip, git, plugins)
jac add <pkg> 	Add dependency
jac remove <pkg> 	Remove dependency
jac update [pkg] 	Update dependencies to latest compatible versions
jac clean 	Clean build artifacts
jac purge 	Purge global bytecode cache
jac script <name> 	Run project script
Tool Commands#
Command 	Description
jac dot <file> 	Generate graph visualization
jac lsp 	Start language server
jac config 	Manage configuration
jac plugins 	Manage plugins
Plugin System#
Available Plugins#
Plugin 	Package 	Description
byllm 	pip install byllm 	LLM integration
jac-client 	pip install jac-client 	Full-stack web development
jac-scale 	pip install jac-scale 	Production deployment
jac-super 	pip install jac-super 	Enhanced console output
Managing Plugins#

# List plugins
jac
 plugins list

# Enable plugin
jac
 plugins enable byllm

# Disable plugin
jac
 plugins disable byllm

# Plugin info
jac
 plugins info byllm

Plugin Configuration#

In jac.toml:

[plugins.byllm]
enabled = true
default_model = "gpt-4"

[plugins.client]
port = 5173
typescript = false

[plugins.scale]
replicas = 3

Project Configuration#

For the full reference, see Configuration.
jac.toml Structure#

[project]
name = "my-app"
version = "1.0.0"
description = "My Jac application"
entry = "main.jac"

[dependencies]
numpy = "^1.24.0"
pandas = "^2.0.0"

[dependencies.dev]
pytest = "^7.0.0"

[dependencies.npm]
react = "^18.0.0"
"@mui/material" = "^5.0.0"

[plugins.byllm]
default_model = "gpt-4"

[plugins.client]
port = 5173

# Private npm registries (generates .npmrc)
[plugins.client.npm.scoped_registries]
"@mycompany" = "https://npm.pkg.github.com"

[plugins.client.npm.auth."//npm.pkg.github.com/"]
_authToken = "${NODE_AUTH_TOKEN}"

[scripts]
dev = "jac start main.jac --dev"
test = "jac test"
build = "jac build"

[environments.production]
OPENAI_API_KEY = "${OPENAI_API_KEY}"

Running Scripts#

jac
 script dev
jac
 script test
jac
 script build

Configuration Profiles#

Jac supports multi-file configuration with profile-based overrides.

File loading order (lowest to highest priority):
File 	When loaded 	Git tracked?
jac.toml 	Always 	Yes
jac.<profile>.toml 	When --profile or JAC_PROFILE is set 	Yes
[environments.<profile>] in jac.toml 	When profile is set 	Yes
jac.local.toml 	Always if present 	No (gitignored)

Using profiles:

# Via --profile flag
jac
 run --profile prod app.jac
jac
 start --profile staging

# Via JAC_PROFILE environment variable
JAC_PROFILE=ci jac test

# Via jac.toml default
# [environment]
# default_profile = "dev"

Example profile files:
jac.prod.toml
jac.local.toml (gitignored, developer-specific)

[serve]
port = 80

[plugins.byllm]
default_model = "gpt-4"

    Note: JAC_ENV is deprecated. Use JAC_PROFILE instead.

Environment Variables#

Server-side:
Variable 	Description
OPENAI_API_KEY 	OpenAI API key
ANTHROPIC_API_KEY 	Anthropic API key
REDIS_URL 	Redis connection URL
MONGODB_URI 	MongoDB connection URI
JWT_SECRET 	JWT signing secret

Client-side (Vite):

Variables prefixed with VITE_ are exposed to client. Define them in a .env file:

# .env
VITE_API_URL=https://api.example.com

Then access in client code:

cl {
    
def:pub app() -> JsxElement {
        
api_url = import.meta.env.VITE_API_URL;
        
return <div>{api_url}</div>;
    
}
}

JavaScript/npm Interoperability#
npm Packages#

cl {
    
import from react { useState, useEffect, useCallback }
    
import from "@tanstack/react-query" { useQuery, useMutation }
    
import from lodash { debounce, throttle }
    
import from axios { default as axios }
}

TypeScript Configuration#

TypeScript is supported through the jac-client Vite toolchain for client-side code. Configure in jac.toml:

[plugins.client]
typescript = true

    Note: Jac does not parse TypeScript files directly. TypeScript support is provided through Vite's built-in TypeScript handling in client-side (cl {}) code.

Browser APIs#

cl {
    
def:pub app() -> JsxElement {
        
# Window
        
width = window.innerWidth;

        
# LocalStorage
        
window.localStorage.setItem("key", "value");
        
value = window.localStorage.getItem("key");

        
# Document
        
element = document.getElementById("my-id");

        
return <div>{width}</div>;
    
}

    
# Fetch
    
async def load_data() -> None {
        
response = await fetch("/api/data");
        
data = await response.json();
    
}
}

IDE & AI Tool Integration#

Jac is a new language, so AI coding assistants may hallucinate syntax from outdated or nonexistent versions. The Jaseci team maintains an official condensed language reference designed for LLM context windows: jaseci-llmdocs.
Setup#

Grab the latest candidate.txt and add it to your AI tool's persistent context:

curl
 -LO https://github.com/jaseci-labs/jaseci-llmdocs/releases/latest/download/candidate.txt

Context File Locations#
Tool 	Context File
Claude Code 	CLAUDE.md in project root (or ~/.claude/CLAUDE.md for global)
Gemini CLI 	GEMINI.md in project root (or ~/.gemini/GEMINI.md for global)
Cursor 	.cursor/rules/jac-reference.mdc (or Settings > Rules)
Antigravity 	GEMINI.md in project root (or .antigravity/rules.md)
OpenAI Codex 	AGENTS.md in project root (or ~/.codex/AGENTS.md for global)
Quick Setup Commands#

# Claude Code
cat
 candidate.txt >> CLAUDE.md

# Gemini CLI
cat
 candidate.txt >> GEMINI.md

# Cursor
mkdir
 -p .cursor/rules && cp candidate.txt .cursor/rules/jac-reference.mdc

# Antigravity
cat
 candidate.txt >> GEMINI.md

# OpenAI Codex
cat
 candidate.txt >> AGENTS.md

When you update Jac, pull a fresh copy from the releases page to stay current.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Foundation
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
            Foundation
            Primitives & Codespace Semantics
            Functions & Objects
            Object-Spatial Programming
            Concurrency
            Comprehensions & Filters
            Learn by Doing
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Introduction
        1 What is Jac?
        2 The Six Principles
        3 Designed for Humans and AI
        4 When to Use Jac
        5 Jac vs Python
    Getting Started
        1 Installation
        2 Your First Program
        3 Project Structure
        4 Editor Setup
    Language Basics
        1 Source Code Encoding
        2 Comments
        3 Statements and Expressions
        4 Code Blocks
        5 Keywords
        6 Identifiers
        7 Entry Point Variants
    Types and Values
        1 Builtin Types
        2 Type Annotations
        3 Generic Types
        4 Union Types
        5 Type References
        6 Literals
        7 F-String Format Specifications
    Variables and Scope
        1 Local Variables
        2 Instance Variables (has)
        3 Global Variables (glob)
        4 Scope Rules
        5 Truthiness
    Operators
        1 Arithmetic Operators
        2 Comparison Operators
        3 Logical Operators
        4 Bitwise Operators
        5 Assignment Operators
        6 Null-Safe Operators
        7 Graph Operators (OSP)
        8 Pipe Operators
        9 The by Operator
        10 Operator Precedence
    Control Flow
        1 Conditional Statements
        2 While Loops
        3 For Loops
        4 Pattern Matching
        5 Switch Statement
        6 Loop Control
        7 Context Managers
        8 Exception Handling
        9 Assertions
        10 Generator Functions
    Native Compilation
        .na.jac Files
        Supported Features
        C Library Imports
        Python-Native Interop
        Standalone Binaries
    Learn More

    Full Reference
    Language Specification

Part I: Foundation#

In this part:

    Introduction - What is Jac, principles, comparison to Python
    Getting Started - Installation, first program, CLI basics
    Language Basics - Syntax, comments, code structure
    Types and Values - Type system, generics, literals
    Variables and Scope - Local, instance, global variables
    Operators - Arithmetic, comparison, logical, graph operators
    Control Flow - Conditionals, loops, pattern matching

Introduction#
1 What is Jac?#

Jac is an AI-native full-stack programming language that supersets Python and JavaScript with native compilation support. It introduces Object-Spatial Programming (OSP) and novel constructs for AI-integrated programming (such as by llm()), providing a unified language for backend, frontend, and AI development with full access to the PyPI and npm ecosystems.

with entry {
    
print("Hello, Jac!");
}

2 The Six Principles#
Principle 	Description
AI-Native 	LLMs as first-class citizens through Meaning Typed Programming
Full-Stack 	Backend and frontend in one unified language
Superset 	Full access to PyPI and npm ecosystems
Object-Spatial 	Graph-based domain modeling with mobile walkers
Cloud-Native 	One-command deployment with automatic scaling
Human & AI Friendly 	Readable structure for both humans and AI models
3 Designed for Humans and AI#

Jac is built for clarity and architectural transparency:

    has declarations for clean attribute definitions
    impl separation keeps interfaces distinct from implementations
    Structure that humans can reason about AND models can reliably generate

4 When to Use Jac#

Jac excels at:

    Graph-structured applications (social networks, knowledge graphs)
    AI-powered applications with LLM integration
    Full-stack web applications
    Agentic AI systems
    Rapid prototyping

5 Jac vs Python#

obj Person {
    
has name: str;
    
has age: int;

    
def greet() -> str {
        
return f"Hi, I'm {self.name}";
    
}
}

Key differences from Python:
Feature 	Python 	Jac
Blocks 	Indentation 	Braces {}
Statements 	Newline-terminated 	Semicolons required
Fields 	self.x = x 	has x: Type;
Methods 	def method(): 	def method() { }
Abilities 	N/A 	can (walker entry/exit only)
Types 	Optional 	Mandatory
Getting Started#
1 Installation#

# Full installation with all plugins
pip
 install jaseci

# Minimal installation
pip
 install jaclang

# Individual plugins
pip
 install byllm        # LLM integration
pip
 install jac-client   # Full-stack web
pip
 install jac-scale    # Production deployment

2 Your First Program#

Create a file hello.jac:

def greet(name: str) -> str {
    
return f"Hello, {name}!";
}

with entry {
    
print(greet("World"));
}

Run it:

jac
 hello.jac

Note: jac is shorthand for jac run.
3 Project Structure#

my_project/
├── jac.toml           # Project configuration
├── main.jac           # Entry point
├── app.jac            # Full-stack entry (jac-client)
├── models/
│   ├── __init__.jac
│   └── user.jac
└── tests/
    └── test_models.jac

File Extensions:
Extension 	Purpose
.jac 	Universal Jac code (head module)
.sv.jac 	Server-variant code
.cl.jac 	Client-variant code
.na.jac 	Native-variant code (compiles to LLVM IR, JIT-executed)
.impl.jac 	Implementation file (annex)
.test.jac 	Test file (annex)

Files sharing the same base name form a single logical module. For example, mymod.jac, mymod.sv.jac, mymod.cl.jac, mymod.impl.jac, and mymod.test.jac are all part of the mymod module. Variant files (.sv.jac, .cl.jac, .na.jac) are automatically discovered and merged during compilation -- see Variant Modules for details.
4 Editor Setup#

Install the VS Code extension for Jac language support:

# Start the language server
jac
 lsp

Language Basics#
1 Source Code Encoding#

Jac source files are UTF-8 encoded. Unicode is fully supported in strings and comments.
2 Comments#

# Single-line comment

#* Multi-line
   comment *#

"""Docstring for modules, classes, and functions"""

Coming from Python

The biggest syntactic differences: Jac uses braces { } instead of indentation for blocks, and semicolons ; to terminate statements. Everything else -- variables, control flow, imports -- is very similar to Python.
3 Statements and Expressions#

All statements end with semicolons:

with entry {
    
x = 5;
    
print(x);
    
result = compute(x) + 10;
}

4 Code Blocks#

Code blocks use braces:

with entry {
    
if condition {
        
statement1;
        
statement2;
    
}
}

5 Keywords#

Jac keywords are reserved and cannot be used as identifiers:
Category 	Keywords
Archetypes 	obj, node, edge, walker, class, enum
Abilities 	can, def, init, postinit
Access 	pub, priv, protect, static, override, abs
Control 	if, elif, else, while, for, match, case, switch, default
Loop 	break, continue
Return 	return, yield, report, skip
Exception 	try, except, finally, raise, assert
OSP 	visit, disengage, spawn, here, root, visitor, entry, exit
Module 	import, include, from, as, glob
Blocks 	cl (client), sv (server), na (native)
Other 	with, test, impl, sem, by, del, in, is, and, or, not, async, await, flow, wait, lambda, props

Note: The abstract modifier keyword is abs, not abstract.
6 Identifiers#

Valid identifiers start with a letter or underscore, followed by letters, digits, or underscores.

To use a reserved keyword as an identifier, escape it with a backtick prefix:

obj Example {
    
has `class: str;  # Backtick-escaped keyword used as identifier
}

Warning

Backtick-escaped keywords in has declarations may cause runtime issues with the underlying dataclass machinery. Use with caution and consider choosing a non-keyword identifier instead.
7 Entry Point Variants#

Entry points define where code execution begins. Unlike Python's if __name__ == "__main__" pattern, Jac provides explicit entry block syntax. Use entry for code that always runs, entry:__main__ for main-module-only code (like tests or CLI scripts), and named entries for exposing multiple entry points from a single file.

Coming from Python

Python's if __name__ == "__main__": becomes with entry:__main__ { }. Plain with entry { } runs every time the module loads (like top-level Python code).

# Default entry - always runs when this module loads
with entry {
    
print("Always runs");
}

# Main entry - only runs when this file is executed directly
# Similar to Python's if __name__ == "__main__"
with entry:__main__ {
    
print("Only when this file is main");
}

Types and Values#

Jac is statically typed -- all variables, fields, and function signatures require type annotations. This enables better tooling, clearer APIs, and catches errors at compile time rather than runtime. The type system is compatible with Python's typing module.
1 Builtin Types#
Type 	Description 	Example
int 	Integer 	42, -17, 0x1F
float 	Floating point 	3.14, 1e-10
str 	String 	"hello", 'world'
bool 	Boolean 	True, False
bytes 	Byte sequence 	b"data"
list 	Mutable sequence 	[1, 2, 3]
tuple 	Immutable sequence 	(1, 2, 3)
set 	Unique values 	{1, 2, 3}
dict 	Key-value mapping 	{"a": 1}
any 	Any type 	--
type 	Type object 	--
None 	Null value 	None

Fixed-width types (for native code and C interop):
Type 	Description 	C Equivalent
i8, u8 	8-bit signed/unsigned integer 	int8_t, uint8_t
i16, u16 	16-bit signed/unsigned integer 	int16_t, uint16_t
i32, u32 	32-bit signed/unsigned integer 	int32_t, uint32_t
i64, u64 	64-bit signed/unsigned integer 	int64_t, uint64_t
f32 	32-bit float 	float
f64 	64-bit float 	double
c_void 	Opaque pointer 	void*

These types are used in .na.jac files for C library interop. The compiler automatically coerces between Jac's standard types (int = i64, float = f64) and fixed-width types at call boundaries.
2 Type Annotations#

Type annotations are required for fields and function signatures:

obj Example {
    
has name: str;
    
has count: int = 0;
    
has items: list[str] = [];
    
has mapping: dict[str, int] = {};
}

3 Generic Types#

Jac will support generic type parameters using Python-style syntax (coming soon):

# Generic function (coming soon):
# def first[T](items: list[T]) -> T {
#     return items[0];
# }

# Generic object (coming soon):
# obj Container[T] {
#     has value: T;
# }

# For now, use `any` as a placeholder:
def first(items: list) -> any {
    
return items[0];
}

obj Container {
    
has value: any;
}

4 Union Types#

obj Example {
    
has value: int | str | None;
}

def process(data: list[int] | dict[str, int]) -> None {
    
# Handle either type
}

5 Type References#

Type references are used in OSP operations like filtering graph traversals by node type. The Root keyword refers to the root node type in entry/exit clauses, and the (?:TypeName) syntax filters collections or traversals by type.

def example() {
    
# In edge references
    
[-->](?:Person);  # Filter nodes by Person type
}

6 Literals#

Numbers:

def example() {
    
decimal = 42;
    
hex = 0x2A;
    
octal = 0o52;
    
binary = 0b101010;
    
floating = 3.14159;
    
scientific = 1.5e-10;

    
# Underscore separators (for readability)
    
million = 1_000_000;
    
hex_word = 0xFF_FF;
}

Strings:

def example() {
    
regular = "hello\nworld";
    
raw = r"no\escape";
    
bytes_lit = b"binary data";
    
x = 42;
    
f_string = f"Value: {x}";
    
multiline = """
        Multiple
        lines
    """;
}

7 F-String Format Specifications#

F-strings support powerful formatting with the syntax {expression:format_spec}.

Basic formatting:

def example() {
    
name = "Alice";
    
age = 30;

    
# Simple interpolation
    
greeting = f"Hello, {name}!";

    
# With expressions
    
message = f"In 5 years: {age + 5}";
}

Width and alignment:

def example() {
    
name = "Alice";
    
# Width specification
    
f"{name:10}";           # "Alice     " (10 chars, left-aligned)
    
f"{name:>10}";          # "     Alice" (right-aligned)
    
f"{name:^10}";          # "  Alice   " (centered)
    
f"{name:<10}";          # "Alice     " (left-aligned, explicit)

    
# Fill character
    
f"{name:*>10}";         # "*****Alice" (fill with *)
    
f"{name:-^10}";         # "--Alice---" (centered with -)
}

Number formatting:

def example() {
    
n = 42;
    
pi = 3.14159265;

    
# Integer formats
    
f"{n:d}";               # "42" (decimal)
    
f"{n:b}";               # "101010" (binary)
    
f"{n:o}";               # "52" (octal)
    
f"{n:x}";               # "2a" (hex lowercase)
    
f"{n:X}";               # "2A" (hex uppercase)
    
f"{n:05d}";             # "00042" (zero-padded, width 5)

    
# Float formats
    
f"{pi:f}";              # "3.141593" (fixed-point, 6 decimals default)
    
f"{pi:.2f}";            # "3.14" (2 decimal places)
    
f"{pi:10.2f}";          # "      3.14" (width 10, 2 decimals)
    
f"{pi:e}";              # "3.141593e+00" (scientific notation)
    
f"{pi:.2e}";            # "3.14e+00" (scientific, 2 decimals)
    
f"{pi:g}";              # "3.14159" (general format)

    
# Percentage
    
ratio = 0.756;
    
f"{ratio:.1%}";         # "75.6%"

    
# Thousands separator
    
big = 1234567;
    
f"{big:,}";             # "1,234,567"
    
f"{big:_}";             # "1_234_567" (underscore separator)
}

Sign and padding:

def example() {
    
x = 42;
    
y = -42;

    
f"{x:+}";               # "+42" (always show sign)
    
f"{y:+}";               # "-42"
    
f"{x:05}";              # "00042" (zero-padded)
}

Conversions (!r, !s, !a):

def example() {
    
text = "hello\nworld";

    
f"{text}";              # "hello\nworld" (default str())
    
f"{text!s}";            # "hello\nworld" (explicit str())
    
f"{text!r}";            # "'hello\\nworld'" (repr())
    
f"{text!a}";            # "'hello\\nworld'" (ascii())
}

Nested expressions:

def example() {
    
width = 10;
    
pi = 3.14159;

    
# Dynamic width
    
f"{pi:{width}}";   # "   3.14159"

    
# Expression in format
    
value = "test";
    
f"{value:>10}";    # "      test"
}

Format specification grammar:

[[fill]align][sign][#][0][width][grouping][.precision][type]

fill      : any character
align     : '<' (left) | '>' (right) | '^' (center) | '=' (pad after sign)
sign      : '+' | '-' | ' '
#         : alternate form (0x for hex, etc.)
0         : zero-pad
width     : minimum width
grouping  : ',' or '_' for thousands
precision : digits after decimal
type      : 's' 'd' 'f' 'e' 'g' 'b' 'o' 'x' 'X' '%'

Collections:

def example() {
    
list_lit = [1, 2, 3];
    
tuple_lit = (1, 2, 3);
    
set_lit = {1, 2, 3};
    
dict_lit = {"key": "value", "num": 42};
    
empty_dict: dict = {};
    
empty_list: list = [];
}

Try it: Literals and collections

Variables and Scope#

Jac distinguishes between local variables (within functions), instance variables (has declarations in objects), and global variables (glob). Unlike Python where you assign self.x = value in __init__, Jac uses declarative has statements that make your data model explicit and visible at a glance.
1 Local Variables#

def example() {
    
# Type inferred
    
x = 42;
    
name = "Alice";

    
# Explicit type
    
count: int = 0;
    
items: list[str] = [];
}

2 Instance Variables (has)#

The has keyword declares instance variables in a clean, declarative style. Unlike Python's self.x = value pattern scattered throughout __init__, has statements appear at the top of your class definition, making the data model immediately visible. This design improves readability for both humans and AI code generators.

Coming from Python

In Python you write self.x = value inside __init__. In Jac, has x: Type = value; at the top of an obj replaces both the __init__ parameter and the assignment -- no self needed for declarations.

obj Person {
    
has name: str;                    # Required
    
has age: int = 0;                 # With default
    
static has count: int = 0;        # Static (class-level)
}

Deferred Initialization:

Use by postinit when a field depends on other fields:

obj Rectangle {
    
has width: float;
    
has height: float;
    
has area: float by postinit;

    
def postinit {
        
self.area = self.width * self.height;
    
}
}

3 Global Variables (glob)#

The glob keyword declares module-level variables, replacing Python's convention of bare global assignments.

Coming from Python

Python uses plain global assignment (DEBUG = True) and the global keyword inside functions. Jac uses glob for declarations (glob DEBUG: bool = True;) and still uses global inside functions to modify them.

glob PI: float = 3.14159;
glob config: dict = {};

with entry {
    
print(PI);
}

4 Scope Rules#

Scope Resolution Order (LEGB):

When Jac looks up a name, it searches in this order:

    Local: Names in the current function/block
    Enclosing: Names in enclosing functions (for nested functions)
    Global: Names at module level (glob declarations)
    Built-in: Pre-defined names (print, len, range, etc.)

glob x = "global";

def outer -> None {
    
x = "enclosing";

    
def inner -> None {
        
x = "local";
        
print(x);  # "local" - found in Local scope
    
}

    
inner();
    
print(x);  # "enclosing" - found in Enclosing scope
}

Modifying outer scope variables:

glob counter: int = 0;

def increment -> None {
    
global counter;    # Declares intent to modify global
    
counter += 1;
}

def outer -> None {
    
x = 10;
    
def inner -> None {
        
nonlocal x;    # Declares intent to modify enclosing
        
x += 1;
    
}
    
inner();
    
print(x);  # 11
}

Block scope behavior:

def example() {
    
if True {
        
block_var = 42;    # Created in block
    
}
    
# block_var is still accessible here in Jac (unlike some languages)

    
for i in range(3) {
        
loop_var = i;
    
}
    
# loop_var and i are accessible here
}

5 Truthiness#

Values are evaluated as boolean in conditions. The following are falsy (evaluate to False):
Type 	Falsy Values
bool 	False
None 	None
int 	0
float 	0.0
str 	"" (empty string)
list 	[] (empty list)
tuple 	() (empty tuple)
dict 	{} (empty dict)
set 	set() (empty set)

All other values are truthy.

Examples:

def example() {
    
# Falsy values
    
if not 0 { print("0 is falsy"); }
    
if not "" { print("empty string is falsy"); }
    
if not [] { print("empty list is falsy"); }
    
if not None { print("None is falsy"); }

    
# Truthy values
    
if 1 { print("non-zero is truthy"); }
    
if "hello" { print("non-empty string is truthy"); }
    
if [1, 2] { print("non-empty list is truthy"); }

    
# Common patterns
    
items = [1, 2, 3];
    
if items {
        
print(items);
    
} else {
        
print("No items to process");
    
}

    
# Default value pattern
    
user_input = "";
    
name = user_input or "Anonymous";
}

Operators#

Jac includes all standard Python operators plus several unique operators for graph manipulation (++>, -->, etc.), null-safe access (?., ?[]), piping (|>, :>), and LLM delegation (by). These Jac-specific operators are covered in sections 6.6-6.9.
1 Arithmetic Operators#
Operator 	Description 	Example
+ 	Addition 	a + b
- 	Subtraction 	a - b
* 	Multiplication 	a * b
/ 	Division 	a / b
// 	Floor division 	a // b
% 	Modulo 	a % b
** 	Exponentiation 	a ** b
@ 	Matrix multiplication 	a @ b
2 Comparison Operators#
Operator 	Description
== 	Equal
!= 	Not equal
< 	Less than
> 	Greater than
<= 	Less than or equal
>= 	Greater than or equal
is 	Identity
is not 	Not identity
in 	Membership
not in 	Not membership
3 Logical Operators#

def example() {
    
a = True;
    
b = False;

    
# Word form (preferred)
    
result = a and b;
    
result = a or b;
    
result = not a;

    
# Symbol form (also valid)
    
result = a && b;
    
result = a || b;
}

4 Bitwise Operators#
Operator 	Name 	Description
& 	AND 	1 if both bits are 1
\| 	OR 	1 if either bit is 1
^ 	XOR 	1 if bits are different
~ 	NOT 	Inverts all bits
<< 	Left shift 	Shifts bits left, fills with 0
>> 	Right shift 	Shifts bits right

Examples:

def example() {
    
flags = 0b1010;
    
FLAG_MASK = 0b0010;
    
NEW_FLAG = 0b0100;
    
value = 16;

    
# Bitwise AND - check if bit is set
    
has_flag = (flags & FLAG_MASK) != 0;

    
# Bitwise OR - set a bit
    
flags = flags | NEW_FLAG;

    
# Bitwise XOR - toggle a bit
    
flags = flags ^ FLAG_MASK;

    
# Bitwise NOT - invert all bits
    
inverted = ~value;

    
# Left shift - multiply by 2^n
    
doubled = value << 1;      # value * 2
    
quadrupled = value << 2;   # value * 4

    
# Right shift - divide by 2^n
    
halved = value >> 1;       # value // 2
    
quartered = value >> 2;    # value // 4
}

Common bit manipulation patterns:

# Check if nth bit is set
def is_bit_set(value: int, n: int) -> bool {
    
return (value & (1 << n)) != 0;
}

# Set nth bit
def set_bit(value: int, n: int) -> int {
    
return value | (1 << n);
}

# Clear nth bit
def clear_bit(value: int, n: int) -> int {
    
return value & ~(1 << n);
}

# Toggle nth bit
def toggle_bit(value: int, n: int) -> int {
    
return value ^ (1 << n);
}

# Check if power of 2
def is_power_of_two(n: int) -> bool {
    
return n > 0 and (n & (n - 1)) == 0;
}

5 Assignment Operators#

Simple Assignment:

def example() {
    
x = 5;
    
name = "Alice";
    
a = b = c = 0;  # Chained assignment
}

Walrus Operator (:=):

The walrus operator assigns a value and returns it in a single expression:

def example() {
    
items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];

    
# In conditionals - assign and test
    
if (n := len(items)) > 10 {
        
print(f"List has {n} items, too many!");
    
}

    
# In comprehensions
    
data = [1, 2, 3];
    
results = [y for x in data if (y := x * 2) > 2];

    
# In function calls
    
text = "hello";
    
print(f"Length: {(n := len(text))}, doubled: {n * 2}");
}

Augmented Assignment Operators:

All augmented assignments modify the variable in place:
Operator 	Equivalent 	Description
x += y 	x = x + y 	Add and assign
x -= y 	x = x - y 	Subtract and assign
x *= y 	x = x * y 	Multiply and assign
x /= y 	x = x / y 	Divide and assign
x //= y 	x = x // y 	Floor divide and assign
x %= y 	x = x % y 	Modulo and assign
x **= y 	x = x ** y 	Exponentiate and assign
x @= y 	x = x @ y 	Matrix multiply and assign
x &= y 	x = x & y 	Bitwise AND and assign
x \|= y 	x = x \| y 	Bitwise OR and assign
x ^= y 	x = x ^ y 	Bitwise XOR and assign
x <<= y 	x = x << y 	Left shift and assign
x >>= y 	x = x >> y 	Right shift and assign

def example() {
    
count = 0;
    
total = 100.0;
    
tax_rate = 1.08;
    
value = 2;
    
flags = 0b0000;
    
NEW_FLAG = 0b0100;
    
OLD_FLAG = 0b0010;
    
bits = 0b1010;
    
mask = 0b0011;
    
register = 1;

    
# Numeric augmented assignment
    
count += 1;
    
total *= tax_rate;
    
value **= 2;

    
# Bitwise augmented assignment
    
flags |= NEW_FLAG;      # Set a flag
    
flags &= ~OLD_FLAG;     # Clear a flag
    
bits ^= mask;           # Toggle bits
    
register <<= 4;         # Shift left
}

6 Null-Safe Operators#

The ? operator provides safe access to potentially null values, returning None instead of raising an error.

Safe attribute access (?.):

obj Profile {
    
has settings: dict = {};
}

obj User {
    
has profile: Profile | None = None;
}

def example(obj: User | None, user: User | None) {
    
# Without null-safe: raises AttributeError if obj is None
    
value = obj.profile;

    
# With null-safe: returns None if obj is None
    
value = obj?.profile;

    
# Chained - stops at first None
    
result = user?.profile?.settings;
}

Safe index access (?[]):

The ?[] operator safely handles both None containers and invalid subscripts. It returns None instead of raising IndexError, KeyError, or TypeError:

def example(my_list: list | None, config: dict | None) {
    
# Without null-safe: raises TypeError if list is None
    
item = my_list[0];

    
# With null-safe: returns None if list is None
    
item = my_list?[0];

    
# Works with dictionaries too
    
value = config?["key"];

    
# Also handles out-of-bounds indices
    
items = [1, 2, 3];
    
result = items?[10];         # None (no IndexError)

    
# And missing dictionary keys
    
data = {"a": 1};
    
result = data?["missing"];   # None (no KeyError)
}

Safe method calls:

obj Data {
    
def transform(param: str) -> Data {
        
return self;
    
}
    
def format() -> str {
        
return "formatted";
    
}
}

def example(obj: Data | None, data: Data | None) {
    
# Returns None if obj is None, doesn't call method
    
result = obj?.transform("x");

    
# Chained with arguments
    
output = data?.transform("param")?.format();
}

Combining with default values:

obj User {
    
has name: str = "";
    
has is_active: bool = True;
}

def example(user: User | None) {
    
# Null-safe with fallback using or
    
name = user?.name or "Anonymous";

    
# In conditionals
    
if user?.is_active {
        
print(user);
    
}
}

In filter comprehensions:

obj Item {
    
has value: int = 0;
}

def example() {
    
items = [Item(value=1), Item(value=-1), Item(value=2)];
    
# The ? in filter comprehensions
    
valid_items = items(?value > 0);  # Filter where value > 0
}

Behavior summary:
Expression 	When obj is None 	When obj is valid
obj?.attr 	None 	obj.attr
obj?[key] 	None 	obj[key]
obj?.method() 	None 	obj.method()
obj?.a?.b 	None 	obj.a.b (or None if a is None)
7 Graph Operators (OSP)#

Graph operators are fundamental to Object-Spatial Programming. They let you create connections between nodes (++>) and traverse the graph (-->). Unlike traditional object references, graph connections are first-class entities that can have their own types and attributes. Use these operators whenever you're building or navigating graph structures.

Connection Operators:

node Person {
    
has name: str;
}

edge Friend {
    
has since: int = 2020;
}

with entry {
    
node1 = Person(name="Alice");
    
node2 = Person(name="Bob");

    
# Untyped connections
    
node1 ++> node2;         # Forward
    
node1 <++ node2;         # Backward
    
node1 <++> node2;        # Bidirectional

    
# Typed connections
    
alice = Person(name="Alice");
    
bob = Person(name="Bob");
    
alice +>: Friend(since=2020) :+> bob;
}

Edge Reference Operators:

node Item {
    
has value: int = 0;
}

edge Link {
    
has weight: int = 1;
}

walker Visitor {
    
can visit with Item entry {
        
# All outgoing edges
        
neighbors = [-->];

        
# All incoming edges
        
sources = [<--];

        
# Typed outgoing
        
linked = [->:Link:->];

        
# Filtered by edge attribute
        
heavy = [->:Link:weight > 5:->];
    
}
}

8 Pipe Operators#

Pipe operators enable functional-style data transformation by passing results from one operation to the next. Instead of deeply nested function calls like format(filter(transform(data))), you write data |> transform |> filter |> format -- reading naturally from left to right. Jac offers three pipe variants: standard pipes for functions, atomic pipes for controlling walker traversal order, and dot pipes for method chaining.

Standard Pipes (|>, <|):

def double(x: int) -> int { return x * 2; }
def add_one(x: int) -> int { return x + 1; }

def example() {
    
data = 5;

    
# Forward pipe - data flows left to right
    
result = data |> double |> add_one;

    
# Equivalent to:
    
result = add_one(double(data));
}

Atomic Pipes (:>, <:):

Atomic pipes are used with spawn operations and affect traversal order:

node Item {
    
has value: int = 0;
}

walker Visitor {
    
can visit with Item entry {
        
print(here.value);
    
}
}

with entry {
    
start = Item(value=1);

    
# Atomic pipe forward - depth-first traversal
    
start spawn :> Visitor();

    
# Standard pipe with spawn - breadth-first traversal
    
start spawn |> Visitor();
}

Dot Pipes (.>, <.):

Dot pipes chain method calls:

obj Builder {
    
has value: int = 0;

    
def add(n: int) -> Builder {
        
self.value += n;
        
return self;
    
}
    
def double() -> Builder {
        
self.value *= 2;
        
return self;
    
}
}

def example() {
    
# Dot forward pipe
    
result = Builder() .> add(5) .> double();

    
# Equivalent to:
    
result = Builder().add(5).double();
}

Pipe with lambdas:

def example() {
    
numbers = [1, 2, 3, 4, 5, 6, 7, 8];

    
# Using lambdas in pipe chains
    
result = numbers
        
|> (lambda x: list : [i * 2 for i in x])
        
|> (lambda x: list : [i for i in x if i > 10])
        
|> sum;
}

Comparison of pipe operators:
Operator 	Name 	Direction 	Use Case
\|> 	Forward pipe 	Left to right 	Function composition
<\| 	Backward pipe 	Right to left 	Reverse composition
:> 	Atomic forward 	Left to right 	Depth-first spawn
<: 	Atomic backward 	Right to left 	Reverse atomic
.> 	Dot forward 	Left to right 	Method chaining
<. 	Dot backward 	Right to left 	Reverse method chain
9 The by Operator#

The by operator is Jac's mechanism for delegation -- handing off work to an external system. Its most powerful use is with the byllm plugin, where by llm delegates function implementation to a language model. This enables "Meaning Typed Programming" where you declare what a function should do, and the LLM provides how. The operator is intentionally generic, allowing plugins to define custom delegation targets.

General Syntax:

def example() {
    
# Basic by expression
    
result = "hello" by "world";

    
# Chained by expressions (right-associative)
    
result = "a" by "b" by "c";  # Parsed as: "a" by ("b" by "c")

    
# With expressions
    
result = (1 + 2) by (3 * 4);
}

With byllm Plugin (LLM Delegation):

When the byllm plugin is installed, by enables LLM delegation:

# Function implementation delegated to LLM
def summarize(text: str) -> str by llm();
sem summarize = "Summarize the given text in 2-3 sentences";

def translate(text: str) -> str by llm(model_name="gpt-4");
sem translate = "Translate the given text to French";

with entry {
    
result = summarize("Hello world");
}

Use the sem keyword to attach semantic descriptions to functions, parameters, and fields. These descriptions are included in the compiler-generated prompt, giving the LLM additional context beyond what it can infer from names and types:

obj Ingredient {
    
has name: str;
    
has cost: float;
}
sem Ingredient.cost = "Estimated cost in USD";

def plan_shopping(recipe: str) -> list[Ingredient] by llm();
sem plan_shopping = "Generate a shopping list for the given recipe";
sem plan_shopping.recipe = "A description of the meal to prepare";

Tip

Always use sem to provide context for by llm() functions. Docstrings are for human documentation and are not included in compiler-generated prompts.

See Part V: AI Integration for detailed LLM usage.
10 Operator Precedence#

Complete precedence table from lowest (evaluated last) to highest (evaluated first):
Precedence 	Operators 	Associativity 	Description
1 (lowest) 	lambda 	- 	Lambda expression
2 	if else 	Right 	Ternary conditional
3 	by 	Right 	By operator (LLM delegation)
4 	:= 	Right 	Walrus operator
5 	or, \|\| 	Left 	Logical OR
6 	and, && 	Left 	Logical AND
7 	not 	- 	Logical NOT (unary)
8 	in, not in, is, is not, <, <=, >, >=, !=, == 	Left 	Comparison/membership
9 	\| 	Left 	Bitwise OR
10 	^ 	Left 	Bitwise XOR
11 	& 	Left 	Bitwise AND
12 	<<, >> 	Left 	Bit shifts
13 	\|>, <\| 	Left 	Pipe operators
14 	+, - 	Left 	Addition, subtraction
15 	*, /, //, %, @ 	Left 	Multiplication, division, modulo, matmul
16 	+x, -x, ~ 	- 	Unary plus, minus, bitwise NOT
17 	** 	Right 	Exponentiation
18 	await 	- 	Await expression
19 	spawn 	Left 	Walker spawn
20 	:>, <: 	Left 	Atomic pipes
21 	++>, <++, connection ops 	Left 	Graph connection
22 (highest) 	x[i], x.attr, x(), x?.attr 	Left 	Subscript, attribute, call

Examples showing precedence:

def f(x: int) -> int { return x + 1; }
def g(x: int) -> int { return x * 2; }

def example() {
    
a = 1; b = 2; c = 3; cond = True;

    
# Ternary binds loosely
    
x = a if cond else b + 1;   # x = a if cond else (b + 1)

    
# Logical operators
    
x = a or b and c;           # x = a or (b and c)
    
x = not a and b;            # x = (not a) and b

    
# Comparison chaining
    
x = 5;
    
valid = 0 < x < 10;         # (0 < x) and (x < 10)

    
# Arithmetic
    
x = a + b * c;              # x = a + (b * c)
    
x = a ** b ** c;            # x = a ** (b ** c)

    
# Bitwise
    
x = a | b & c;              # x = a | (b & c)
    
x = a << 2 + 1;             # x = a << (2 + 1)

    
# Pipe operators
    
result = a |> f |> g;       # result = g(f(a))

    
# Walrus in condition
    
items = [1, 2, 3];
    
if (n := len(items)) > 2 { print(n); }
}

Short-circuit evaluation:

and and or use short-circuit evaluation:

def example() {
    
a = 1; b = 2; c = 3;

    
# 'and' stops at first falsy value
    
result = a and b and c;  # Returns first falsy, or last value

    
# 'or' stops at first truthy value
    
result = a or b or c;    # Returns first truthy, or last value

    
# Common patterns
    
user_input = "";
    
fallback = "fallback";
    
value = user_input or fallback;     # Use fallback if input is falsy
}

Try it: Operators

Control Flow#

Jac's control flow is familiar to Python developers with a few enhancements: braces instead of indentation, semicolons to end statements, and additional constructs like C-style for loops (for i = 0 to i < 10 by i += 1) and switch statements. Jac also supports Python's pattern matching (match/case) for destructuring complex data.
1 Conditional Statements#

def example() {
    
condition = True;
    
other_condition = False;

    
if condition {
        
print("condition true");
    
} elif other_condition {
        
print("other condition");
    
} else {
        
print("else");
    
}

    
# Ternary expression
    
result = "yes" if condition else "no";
}

2 While Loops#

def example() {
    
count = 0;

    
while count < 3 {
        
print(count);
        
count += 1;
    
}

    
# With else clause (executes if loop completes normally)
    
count = 0;
    
while count < 3 {
        
count += 1;
    
} else {
        
print("completed");
    
}
}

3 For Loops#

Jac supports Python-style iteration and also adds C-style for loops with explicit initialization, condition, and update expressions. The C-style syntax uses to for the condition and by for the update step -- useful when you need precise control over loop variables.

def example() {
    
items = [1, 2, 3];

    
# Iterate over collection (Python-style)
    
for item in items {
        
print(item);
    
}

    
# With index
    
for (i, item) in enumerate(items) {
        
print(f"{i}: {item}");
    
}

    
# C-style for loop: for INIT to CONDITION by UPDATE
    
for i = 0 to i < 10 by i += 1 {
        
print(i);
    
}

    
# With else clause
    
for item in items {
        
if item == 5 {
            
break;
        
}
    
} else {
        
print("Not found");
    
}
}

4 Pattern Matching#

Pattern matching lets you destructure and test complex data in a single construct. Unlike a chain of if/elif statements, match can extract values from lists, dicts, and objects while testing their structure. Use it when handling multiple data shapes or implementing state machines.

Common Gotcha

Match case bodies use Python-style indentation, not braces. The case keyword is followed by a colon, and the body is indented -- this is the one place in Jac where indentation matters.

Basic Patterns:

obj Point {
    
has x: int = 0;
    
has y: int = 0;
}

def example(value: any) {
    
match value {
        
case 0:
            
print("zero");

        
case 1 | 2 | 3:
            
print("small");

        
case [x, y]:
            
print(f"pair: {x}, {y}");

        
case {"key": v}:
            
print(f"dict with key: {v}");

        
case Point(x=x, y=y):
            
print(f"point at {x}, {y}");

        
case _:
            
print("default");
    
}
}

Advanced Patterns:

def example(data: any) {
    
match data {
        
case [1, *middle, 5]:              # Spread: capture remainder
            
print(f"Middle: {middle}");

        
case {"key1": 1, **rest}:          # Dict spread
            
print(f"Rest: {rest}");

        
case [1, 2, last as captured]:     # As: bind to name
            
print(f"Captured: {captured}");

        
case [1, 2] | [3, 4]:              # Or: match either
            
print("Matched");
    
}
}

Pattern Types:
Pattern 	Example 	Description
Literal 	case 42: 	Match exact value
Capture 	case x: 	Capture into variable
Wildcard 	case _: 	Match anything, don't capture
Sequence 	case [a, b]: 	Match list/tuple structure
Mapping 	case {"k": v}: 	Match dict structure
Class 	case Point(x, y): 	Match class instance
Or 	case 1 \| 2: 	Match any option
As 	case x as name: 	Capture with alias
Star 	case [first, *rest]: 	Capture sequence remainder
Double-star 	case {**rest}: 	Capture dict remainder
5 Switch Statement#

def example(value: int) {
    
switch value {
        
case 1:
            
print("one");

        
case 2:
            
print("two");

        
default:
            
print("other");
    
}
}

Note: Like C, cases fall through to subsequent cases. Use break to prevent fall-through.
6 Loop Control#

def example() {
    
items = [1, 2, 3, 4, 5];

    
for item in items {
        
if item == 2 {
            
continue;    # Skip to next iteration
        
}
        
if item == 4 {
            
break;       # Exit loop
        
}
        
print(item);
    
}
}

7 Context Managers#

def example() {
    
with open("file.txt") as f {
        
content = f.read();
    
}

    
# Multiple context managers
    
with open("in.txt") as fin, open("out.txt", "w") as fout {
        
fout.write(fin.read());
    
}
}

8 Exception Handling#

Basic try/except:

def risky_operation() -> int {
    
raise ValueError("error");
}

def example() {
    
try {
        
result = risky_operation();
    
} except ValueError {
        
print("Value error occurred");
    
}
}

Capturing the exception:

import json;

def example(input: str) {
    
try {
        
data = json.loads(input);
    
} except ValueError as e {
        
print(f"Parse error: {e}");
    
} except KeyError as e {
        
print(f"Missing key: {e}");
    
}
}

Multiple exception types:

def process(data: any) -> None {
    
print(data);
}

def example(data: any) {
    
try {
        
process(data);
    
} except (TypeError, ValueError) as e {
        
print(f"Type or value error: {e}");
    
}
}

Full try/except/else/finally:

def example() {
    
default_data = "default";
    
file = None;
    
data = "";

    
try {
        
file = open("data.txt");
        
data = file.read();
    
} except FileNotFoundError {
        
print("File not found");
        
data = default_data;
    
} except PermissionError as e {
        
print(f"Permission denied: {e}");
        
raise;  # Re-raise the exception
    
} else {
        
# Executes only if no exception occurred
        
print(f"Read {len(data)} bytes");
    
} finally {
        
# Always executes (cleanup)
        
if file {
            
file.close();
        
}
    
}
}

Raising exceptions:

def validate(input: str) -> None {
    
if not input {
        
# Raise an exception
        
raise ValueError("Invalid input");
    
}
}

def process(item: str) -> None {
    
try {
        
validate(item);
    
} except ValueError as e {
        
# Re-raise with more context
        
raise RuntimeError(f"Failed to process: {item}") from e;
    
}
}

Custom exceptions:

obj ValidationError(Exception) {
    
has field: str;
    
has message: str;
}

def validate(data: dict) -> None {
    
if "name" not in data {
        
raise ValidationError(field="name", message="Name is required");
    
}
}

9 Assertions#

Assertions verify conditions during development:

def example() {
    
condition = True;
    
items = [1, 2, 3];
    
value = 42;

    
# Basic assertion
    
assert condition;

    
# Assertion with message
    
assert len(items) > 0, "Items list cannot be empty";

    
# Type checking
    
assert isinstance(value, int), f"Expected int, got {type(value)}";
}

# Invariant checking in class methods
obj Account {
    
has balance: float = 0.0;

    
def withdraw(amount: float) -> None {
        
assert amount > 0, "Withdrawal amount must be positive";
        
assert amount <= self.balance, "Insufficient funds";
        
self.balance -= amount;
    
}
}

Note: Assertions can be disabled in production with optimization flags. Use exceptions for validation that must always run.
10 Generator Functions#

Generators produce values lazily using yield:

Basic generator:

def count_up(n: int) -> int {
    
for i in range(n) {
        
yield i;
    
}
}

with entry {
    
# Usage
    
for num in count_up(5) {
        
print(num);  # 0, 1, 2, 3, 4
    
}
}

Generator with state:

def fibonacci(limit: int) -> int {
    
a = 0;
    
b = 1;
    
while a < limit {
        
yield a;
        
(a, b) = (b, a + b);
    
}
}

yield from (delegation):

def flatten(nested: list) -> any {
    
for item in nested {
        
if isinstance(item, list) {
            
yield from flatten(item);  # Delegate to sub-generator
        
} else {
            
yield item;
        
}
    
}
}

with entry {
    
# Usage
    
nested = [[1, 2], [3, [4, 5]], 6];
    
flat = list(flatten(nested));  # [1, 2, 3, 4, 5, 6]
}

Generator expressions:

def example() {
    
# Generator expression (lazy)
    
squares = (x ** 2 for x in range(1000000));

    
# List comprehension (eager)
    
squares_list = [x ** 2 for x in range(100)];
}

Try it: Control flow and generators

Native Compilation#

Jac supports compiling to native machine code via LLVM for performance-critical workloads. Native code runs as pure machine code with zero Python interpreter overhead.
.na.jac Files#

Files ending in .na.jac are compiled to native code via LLVM IR:

# Run a native Jac file
jac
 run compute.na.jac

Native code can also be part of a larger module via variant annexing. Given main.jac, a sibling main.na.jac is automatically discovered, compiled, and merged as the native codespace.
Supported Features#

The native backend supports:

    Primitive types: int, float, bool, str
    Fixed-width C types: i8, u8, i16, u16, i32, u32, i64, u64, f32, f64, c_void
    Collections: list, dict, set with literals, subscript, iteration, and comprehensions
    Control flow: if/elif/else, for, while, match
    Functions, closures, and cross-module imports
    Context managers (with statements)
    Python/native interop (native functions can call Python and vice versa)

C Library Imports#

Import C shared libraries directly in native Jac code:

# compute.na.jac
import from "libm" {
    
def sin(x: f64) -> f64;
    
def cos(x: f64) -> f64;
    
def sqrt(x: f64) -> f64;
}

with entry {
    
result = sqrt(sin(1.0) ** 2 + cos(1.0) ** 2);
    
print(result);  # 1.0
}

C structs can be declared inside library import blocks and used as normal Jac objects with automatic value-type coercion at call boundaries:

import from "libgraphics" {
    
obj Color {
        
has r: u8, g: u8, b: u8, a: u8;
    
}
    
def set_pixel(x: i32, y: i32, color: Color) -> c_void;
}

Python-Native Interop#

Native and Python codespaces can call each other within the same module:

# main.jac (Python/server codespace)
sv {
    
def process_data(data: list) -> list {
        
# Python code with full PyPI access
        
return sorted(data);
    
}
}

# main.na.jac (native codespace)
import from ...main { process_data }

with entry {
    
# Native code calling Python function
    
result = process_data([3, 1, 2]);
}

Standalone Binaries#

Self-contained .na.jac files (those with a with entry {} block and no Python dependencies) can be compiled to standalone native executables:

# Compile to a standalone binary
jac
 nacompile program.na.jac

# Run it directly -- no jac or Python needed
./program

The nacompile command requires no external compiler, assembler, or linker. The entire pipeline runs in pure Python:

    The Jac compiler generates LLVM IR from the .na.jac source
    llvmlite emits native object code for the host architecture
    A built-in pure-Python ELF linker produces a dynamically-linked executable

The resulting binary links only against libc at runtime. See jac nacompile for full usage details.
Learn More#

Tutorials:

    Jac Basics - Step-by-step introduction to Jac syntax
    Installation - Setup and your first Jac program

Related Reference:

    Part II: Functions & Objects - Classes, methods, inheritance

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Primitives & Codespace Semantics
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
            Foundation
            Primitives & Codespace Semantics
            Functions & Objects
            Object-Spatial Programming
            Concurrency
            Comprehensions & Filters
            Learn by Doing
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Overview
    Codespace Model
        Cross-Codespace Interop
        What Is Shared
    Primitive Types
        Numeric Types
            int -- Integer
            float -- Floating Point
            complex -- Complex Number
        String and Byte Types
            str -- String
            bytes -- Byte Sequence
        Collection Types
            list -- Mutable Sequence
            dict -- Key-Value Mapping
            set -- Mutable Unordered Collection
            frozenset -- Immutable Set
            tuple -- Immutable Sequence
            range -- Immutable Integer Sequence
        Fixed-Width Types (Native Codespace)
    Operator Semantics
        Arithmetic Operators
        Comparison Operators
        Bitwise Operators
        Membership Operator
    Builtin Functions
        I/O
        Aggregation and Ordering
        Iteration
        Type Checking
        Introspection
        Numeric Conversions
        Type Constructors
        Other
    Backend Contract
        How It Works
        What This Means for You
    Learn More

    Full Reference
    Language Specification

Primitives and Codespace Semantics#

In this part:

    Overview - What are primitives and why they matter across codespaces
    Codespace Model - Server, Client, and Native compilation targets
    Primitive Types - The fixed set of types shared across all codespaces
    Operator Semantics - Uniform operator behavior across backends
    Builtin Functions - Functions available in every codespace
    Backend Contract - How each codespace implements the primitives

Overview#

Jac programs can target multiple execution environments -- a Python-based server, a JavaScript-based browser client, or a native LLVM-compiled binary -- yet all three share the same source language and the same set of primitive types, operators, and builtin functions. This page documents that fixed set of semantics: the contract that every Jac codespace must honor.

The key insight is that Jac's compiler does not simply transpile syntax; it implements a primitive codegen interface -- a collection of abstract emitter classes that each backend (Python/server, ECMAScript/client, Native/LLVM) must subclass. This ensures that an int behaves like an int, a list behaves like a list, and print() works -- regardless of where the code executes.

Jac Source Code

Jac Compiler

Python / Server Backend
sv { }

ECMAScript / Client Backend
cl { }

Native / LLVM Backend
na { }

Shared Primitive Semantics
int, float, str, list, dict, ...
Codespace Model#

A codespace determines where your code runs. You select a codespace with either a file extension or an inline block prefix:
Codespace 	Block Prefix 	File Extension 	Compiles To 	Ecosystem
Server 	sv { } 	.sv.jac or .jac (default) 	Python 	PyPI
Client 	cl { } 	.cl.jac 	JavaScript / TypeScript 	npm
Native 	na { } 	.na.jac 	LLVM IR → machine code 	C ABI

Code outside any block defaults to the server codespace. Any .jac file can mix codespace blocks:

# Server (default codespace)
def add(a: int, b: int) -> int {
    
return a + b;
}

cl {
    
# Client -- compiles to JavaScript
    
def greet(name: str) -> str {
        
return "Hello, " + name;
    
}
}

na {
    
# Native -- compiles to machine code
    
def fast_sum(n: int) -> int {
        
has total: int = 0;
        
for i in range(n) {
            
total += i;
        
}
        
return total;
    
}
}

Cross-Codespace Interop#

When code in one codespace calls a function in another, the compiler generates the interop layer automatically -- HTTP calls between server and client, FFI bridges between Python and native, serialization and deserialization at boundaries.

# Server function
def:pub fetch_items() -> list[dict] {
    
return [{"id": 1, "name": "Item A"}];
}

cl {
    
# Client calls server -- compiler generates the HTTP call
    
async def load() -> None {
        
items = await fetch_items();
    
}
}

What Is Shared#

Regardless of codespace, the following are identical:

    Primitive types -- int, float, str, bool, bytes, list, dict, set, tuple, frozenset, range, complex
    Operator semantics -- + on two ints always means addition; + on two strings always means concatenation
    Builtin functions -- print(), len(), range(), sorted(), etc.
    Type conversion -- int(), str(), float(), bool(), etc.
    Control flow -- if, for, while, match, comprehensions

What differs between codespaces is the underlying implementation: Python objects, JavaScript values, or LLVM IR instructions. The compiler guarantees behavioral equivalence through the primitive emitter contract described below.
Primitive Types#

Jac defines 12 primitive type families. Each type has a fixed set of named methods and operator behaviors that all backends must implement.
Numeric Types#
int -- Integer#

Arbitrary-precision integer (server), 64-bit integer (native), number / BigInt (client).

Named methods:
Method 	Description
bit_length() 	Number of bits needed to represent the value
bit_count() 	Number of set bits (popcount)
to_bytes(length, byteorder) 	Convert to bytes representation
as_integer_ratio() 	Return (numerator, denominator) pair
conjugate() 	Returns the value itself (complex compatibility)
from_bytes(bytes, byteorder) 	Static -- construct int from bytes

Operators:
Category 	Operators
Arithmetic 	+ - * / // % **
Bitwise 	& \| ^ << >>
Comparison 	== != < > <= >=
Unary 	-x +x ~x
float -- Floating Point#

IEEE 754 double-precision (64-bit) across all codespaces.

Named methods:
Method 	Description
is_integer() 	True if the float is an exact integer value
as_integer_ratio() 	Exact (numerator, denominator) pair
conjugate() 	Returns the value itself
hex() 	Hexadecimal string representation
fromhex(s) 	Static -- construct float from hex string

Operators:
Category 	Operators
Arithmetic 	+ - * / // % **
Comparison 	== != < > <= >=
Unary 	-x +x
complex -- Complex Number#

Complex number with real and imaginary parts.

Named methods:
Method 	Description
conjugate() 	Returns the complex conjugate

Operators:
Category 	Operators
Arithmetic 	+ - * / **
Comparison 	== !=
Unary 	-x +x

No ordering on complex

Complex numbers support equality checks but not ordering (<, >, <=, >=) -- this is enforced across all codespaces.
String and Byte Types#
str -- String#

Unicode text string. Immutable.

Named methods:
Category 	Methods
Case conversion 	capitalize(), casefold(), lower(), upper(), title(), swapcase()
Searching 	count(), find(), rfind(), index(), rindex(), startswith(), endswith()
Modification 	replace(), strip(), lstrip(), rstrip(), removeprefix(), removesuffix()
Splitting 	split(), rsplit(), splitlines(), join(), partition(), rpartition()
Formatting 	format(), format_map(), center(), ljust(), rjust(), zfill(), expandtabs()
Character tests 	isalnum(), isalpha(), isascii(), isdecimal(), isdigit(), isidentifier(), islower(), isnumeric(), isprintable(), isspace(), istitle(), isupper()
Encoding 	encode()
Translation 	translate(), maketrans()

Operators:
Operator 	Meaning
+ 	Concatenation
* 	Repetition
% 	printf-style formatting
== != 	Equality
< > <= >= 	Lexicographic comparison
in 	Substring test
bytes -- Byte Sequence#

Immutable sequence of bytes (0-255). Mirrors most str methods but operates on byte values.

Named methods:
Category 	Methods
Encoding 	decode(), hex(), fromhex()
Searching 	count(), find(), rfind(), index(), rindex(), startswith(), endswith()
Modification 	replace(), strip(), lstrip(), rstrip(), removeprefix(), removesuffix()
Splitting 	split(), rsplit(), splitlines(), join(), partition(), rpartition()
Case (ASCII) 	capitalize(), lower(), upper(), title(), swapcase()
Char tests (ASCII) 	isalnum(), isalpha(), isascii(), isdigit(), islower(), isspace(), istitle(), isupper()
Alignment 	center(), ljust(), rjust(), zfill(), expandtabs()
Translation 	translate(), maketrans()

Operators:
Operator 	Meaning
+ 	Concatenation
* 	Repetition
% 	printf-style formatting
== != 	Equality
< > <= >= 	Lexicographic comparison
in 	Byte membership
Collection Types#
list -- Mutable Sequence#

Ordered, mutable collection. Supports indexing, slicing, and iteration.

Named methods:
Method 	Description
append(x) 	Add item to end
extend(iterable) 	Append all items from iterable
insert(i, x) 	Insert item at position
remove(x) 	Remove first occurrence
pop([i]) 	Remove and return item at index
clear() 	Remove all items
index(x) 	Index of first occurrence
count(x) 	Count occurrences
sort() 	Sort in-place
reverse() 	Reverse in-place
copy() 	Shallow copy

Operators:
Operator 	Meaning
+ 	Concatenation
* 	Repetition
== != 	Structural equality
< > <= >= 	Lexicographic comparison
in 	Membership test
+= 	Extend in-place
*= 	Repeat in-place
dict -- Key-Value Mapping#

Ordered mapping from keys to values (insertion order preserved).

Named methods:
Method 	Description
get(key[, default]) 	Get value or default
keys() 	View of keys
values() 	View of values
items() 	View of key-value pairs
pop(key[, default]) 	Remove and return value
popitem() 	Remove and return last pair
setdefault(key[, default]) 	Get or set default
update(mapping) 	Update from another mapping
clear() 	Remove all items
copy() 	Shallow copy
fromkeys(iterable[, value]) 	Static -- create dict from keys

Operators:
Operator 	Meaning
\| 	Merge (returns new dict)
== != 	Structural equality
in 	Key membership
\|= 	Update in-place
set -- Mutable Unordered Collection#

Unordered collection of unique hashable elements.

Named methods:
Category 	Methods
Mutation 	add(), remove(), discard(), pop(), clear()
Set algebra 	union(), intersection(), difference(), symmetric_difference()
In-place algebra 	update(), intersection_update(), difference_update(), symmetric_difference_update()
Tests 	issubset(), issuperset(), isdisjoint(), copy()

Operators:
Operator 	Meaning
\| 	Union
& 	Intersection
- 	Difference
^ 	Symmetric difference
== != 	Set equality
<= < 	Subset / proper subset
>= > 	Superset / proper superset
in 	Membership
\|= &= -= ^= 	In-place variants
frozenset -- Immutable Set#

Same semantics as set but immutable -- no mutation methods and no in-place operators. Supports all the same algebra operators and comparison operators.
tuple -- Immutable Sequence#

Ordered, immutable collection. Supports indexing and iteration.

Named methods:
Method 	Description
count(x) 	Count occurrences
index(x) 	Index of first occurrence

Operators:
Operator 	Meaning
+ 	Concatenation
* 	Repetition
== != 	Structural equality
< > <= >= 	Lexicographic comparison
in 	Membership test
range -- Immutable Integer Sequence#

Lazy integer sequence, typically used in for loops.

Named methods:
Method 	Description
count(x) 	Count occurrences
index(x) 	Index of value

Operators:
Operator 	Meaning
== != 	Equality
in 	Membership test
Fixed-Width Types (Native Codespace)#

The native codespace adds fixed-width types for C interop. These types map directly to hardware registers and C ABI types:
Jac Type 	Width 	Signed 	C Equivalent
i8 	8-bit 	Yes 	int8_t
u8 	8-bit 	No 	uint8_t
i16 	16-bit 	Yes 	int16_t
u16 	16-bit 	No 	uint16_t
i32 	32-bit 	Yes 	int32_t
u32 	32-bit 	No 	uint32_t
i64 	64-bit 	Yes 	int64_t
u64 	64-bit 	No 	uint64_t
f32 	32-bit 	-- 	float
f64 	64-bit 	-- 	double
c_void 	-- 	-- 	void*

The compiler automatically coerces between Jac's standard types (int = i64, float = f64) and fixed-width types at call boundaries.
Operator Semantics#

Operators in Jac have consistent meaning across codespaces. The following table summarizes which operators are defined for each primitive type family:
Arithmetic Operators#
Operator 	int 	float 	complex 	str 	bytes 	list 	tuple
+ 	add 	add 	add 	concat 	concat 	concat 	concat
- 	sub 	sub 	sub 	-- 	-- 	-- 	--
* 	mul 	mul 	mul 	repeat 	repeat 	repeat 	repeat
/ 	truediv 	truediv 	truediv 	-- 	-- 	-- 	--
// 	floordiv 	floordiv 	-- 	-- 	-- 	-- 	--
% 	mod 	mod 	-- 	format 	format 	-- 	--
** 	pow 	pow 	pow 	-- 	-- 	-- 	--
Comparison Operators#
Operator 	int 	float 	complex 	str 	bytes 	list 	tuple 	dict 	set
== != 	yes 	yes 	yes 	yes 	yes 	yes 	yes 	yes 	yes
< > <= >= 	yes 	yes 	no 	lexicographic 	lexicographic 	lexicographic 	lexicographic 	no 	subset/superset
Bitwise Operators#
Operator 	int 	dict 	set
& 	bitwise AND 	-- 	intersection
\| 	bitwise OR 	merge 	union
^ 	bitwise XOR 	-- 	symmetric diff
<< >> 	shift 	-- 	--
~ 	invert 	-- 	--
Membership Operator#

The in operator is defined for all container types:
Type 	x in container tests
str 	Substring containment
bytes 	Byte membership
list 	Element membership
tuple 	Element membership
set / frozenset 	Element membership
dict 	Key membership
range 	Value membership
Builtin Functions#

These functions are available in every codespace. Each backend provides its own implementation, but the behavior is the same:
I/O#
Function 	Description
print(...) 	Output text to the console / debug log
input([prompt]) 	Read a line of text from stdin
Aggregation and Ordering#
Function 	Description
len(x) 	Length of a collection or string
abs(x) 	Absolute value
round(x[, n]) 	Round to n decimal places
min(...) 	Minimum value
max(...) 	Maximum value
sum(iterable) 	Sum of elements
sorted(iterable) 	Return a new sorted list
reversed(seq) 	Reverse iterator
Iteration#
Function 	Description
enumerate(iterable) 	Pairs of (index, value)
zip(...) 	Parallel iteration over multiple iterables
map(fn, iterable) 	Apply function to each element
filter(fn, iterable) 	Keep elements where function returns true
range([start,] stop[, step]) 	Integer sequence
iter(x) 	Get an iterator
next(iterator) 	Get next value from iterator
Type Checking#
Function 	Description
isinstance(obj, type) 	Check if object is instance of type
issubclass(cls, type) 	Check if class is subclass
type(obj) 	Get the type of an object
callable(obj) 	Check if object is callable
Introspection#
Function 	Description
id(obj) 	Unique identity of an object
hash(obj) 	Hash value
repr(obj) 	String representation
getattr(obj, name) 	Get attribute by name
setattr(obj, name, val) 	Set attribute by name
hasattr(obj, name) 	Check attribute existence
delattr(obj, name) 	Delete attribute
vars(obj) 	Dictionary of attributes
dir(obj) 	List of names in scope
Numeric Conversions#
Function 	Description
chr(i) 	Integer to Unicode character
ord(c) 	Character to integer
hex(i) 	Integer to hex string
oct(i) 	Integer to octal string
bin(i) 	Integer to binary string
pow(x, y[, z]) 	Power with optional modulus
divmod(a, b) 	(quotient, remainder) pair
any(iterable) 	True if any element is truthy
all(iterable) 	True if all elements are truthy
Type Constructors#

Every primitive type can be constructed explicitly:
Function 	Description
int(x) 	Convert to integer
float(x) 	Convert to float
str(x) 	Convert to string
bool(x) 	Convert to boolean
list(x) 	Convert to list
dict(x) 	Convert to dict
set(x) 	Convert to set
tuple(x) 	Convert to tuple
frozenset(x) 	Convert to frozenset
bytes(x) 	Convert to bytes
complex(re, im) 	Construct complex number
range(...) 	Construct range
slice(...) 	Construct slice
bytearray(x) 	Construct mutable byte array
Other#
Function 	Description
open(file, mode) 	Open a file
format(value, spec) 	Format a value
ascii(obj) 	ASCII representation
Backend Contract#

The primitive semantics are enforced through a system of abstract emitter classes defined in the compiler. Each class is parameterized on two types:

    V -- the value representation (e.g., str for ECMAScript code generation, ir.Value for LLVM)
    C -- the context type (e.g., ESEmitCtx, NativeEmitCtx)

Each backend must subclass and implement every emitter:

Native Backend

Client Backend

Server Backend

Primitive Emitter Interface

IntEmitter[V, C]

FloatEmitter[V, C]

StrEmitter[V, C]

BytesEmitter[V, C]

ListEmitter[V, C]

DictEmitter[V, C]

SetEmitter[V, C]

FrozensetEmitter[V, C]

TupleEmitter[V, C]

RangeEmitter[V, C]

ComplexEmitter[V, C]

BuiltinEmitter[V, C]

PyIntEmitter

PyStrEmitter

...

ESIntEmitter

ESStrEmitter

...

NativeIntEmitter

NativeStrEmitter

...
How It Works#

    The compiler parses your Jac source and builds a unified AST
    Type resolution determines the type of every expression
    Codespace routing assigns each block of code to its target backend
    Code generation calls the appropriate emitter method -- for example, "hello" + " world" calls StrEmitter.emit_op_add()
    Each backend's emitter produces the correct output for its target: Python string concatenation, JavaScript +, or LLVM @str_concat

If a backend has not yet implemented an operation, the emitter returns None, allowing the dispatch layer to fall back or raise an error at compile time.
What This Means for You#

As a Jac developer, you do not need to think about emitters. The important takeaway is:

    The set of primitive types and their operations is fixed and uniform across all codespaces
    You can write "hello".upper() in server, client, or native code and get the same result
    Operators like +, in, == behave consistently regardless of compilation target
    If a type or operation is available in one codespace, it is available (or will be) in all of them

This is what makes Jac's multi-target compilation practical: you learn one set of types and operations, and they work everywhere.
Learn More#

Related Reference:

    Part I: Foundation - Type system, operators, control flow
    Core Concepts - Conceptual overview of codespaces
    jac-client Reference - Client codespace plugin details
    Appendices - Operator quick reference, keyword reference

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Functions & Objects
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
            Foundation
            Primitives & Codespace Semantics
            Functions & Objects
            Object-Spatial Programming
            Concurrency
            Comprehensions & Filters
            Learn by Doing
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Functions and Abilities
        1 Function Declaration
        2 Docstrings
        3 Parameter Types and Ordering
        4 can vs def
        5 Methods
        6 Static Methods
        7 Lambda Expressions
        8 Immediately Invoked Function Expressions (IIFE)
        9 Decorators
        10 Access Modifiers
    Object-Oriented Programming
        1 Objects (Classes)
        2 Inheritance
        3 Enumerations
        4 Enums with Inline Python
        5 Properties and Encapsulation
    Implementations and Forward Declarations
        1 Forward Declarations
        2 Implementation Blocks
        3 Separate Implementation Files
        4 Variant Modules
            Native Variant Files (.na.jac)
        5 When to Use Implementations
    Learn More

    Full Reference
    Language Specification

Part II: Functions and Objects#

In this part:

    Functions and Abilities - Function declaration, parameters, abilities
    Object-Oriented Programming - Objects, inheritance, enums
    Implementations and Forward Declarations - Impl blocks, separation of interface

This part covers Jac's approach to functions and object-oriented programming. Jac uses def for standalone functions and can for methods (called "abilities") on objects. The key difference from Python: has declarations make your data model explicit, and impl blocks let you separate interface from implementation.
Functions and Abilities#

Functions in Jac use familiar def syntax with mandatory type annotations. Jac also introduces "abilities" (can) for methods attached to objects, nodes, edges, and walkers. Abilities can be triggered automatically based on context (like when a walker visits a node) rather than being called explicitly.
1 Function Declaration#

def add(a: int, b: int) -> int {
    
return a + b;
}

def greet(name: str) -> str {
    
return f"Hello, {name}!";
}

# No return value
def log(message: str) -> None {
    
print(f"[LOG] {message}");
}

2 Docstrings#

Docstrings appear before declarations (not inside like Python):

"""Module-level docstring."""

"Function docstring."
def add(a: int, b: int) -> int {
    
return a + b;
}

"Object docstring."
obj Person {
    
has name: str;
}

3 Parameter Types and Ordering#

Parameter Categories:
Category 	Syntax 	Description
Positional-only 	Before / 	Must be passed by position
Positional-or-keyword 	Normal params 	Can be passed either way
Variadic positional 	*args 	Collects extra positional args
Keyword-only 	After * or *args 	Must be passed by keyword
Variadic keyword 	**kwargs 	Collects extra keyword args

Required Parameter Order:

def complete_example(
    
pos_only1: int,           # 1. Positional-only parameters
    
pos_only2: str,
    
/,                         # 2. Positional-only marker
    
pos_or_kw: float,          # 3. Normal (positional-or-keyword)
    
with_default: int = 10,    # 4. Parameters with defaults
    
*args: int,                # 5. Variadic positional
    
kw_only: str,              # 6. Keyword-only (after * or *args)
    
kw_default: bool = True,   # 7. Keyword-only with default
    
**kwargs: any              # 8. Variadic keyword (must be last)
) -> None {
    
print("called");
}

Positional-only parameters (/):

def greet(name: str, /) -> str {
    
return f"Hello, {name}!";
}

with entry {
    
greet("Alice");      # OK
    
# greet(name="Alice"); # Error: positional-only
}

Keyword-only parameters (after *):

def configure(*, host: str, port: int = 8080) -> None {
    
print(f"Connecting to {host}:{port}");
}

with entry {
    
configure(host="localhost");           # OK
    
# configure("localhost", 8080);        # Error: keyword-only
    
configure(host="localhost", port=443); # OK
}

Variadic parameters:

# *args collects extra positional arguments
def sum_all(*values: int) -> int {
    
return sum(values);
}

# **kwargs collects extra keyword arguments
def build_config(**options: any) -> dict {
    
return dict(options);
}

# Combined
def flexible(required: int, *args: int, **kwargs: any) -> None {
    
print(f"Required: {required}");
    
print(f"Extra positional: {args}");
    
print(f"Extra keyword: {kwargs}");
}

with entry {
    
sum_all(1, 2, 3, 4, 5);  # 15
    
build_config(debug=True, verbose=False);  # {"debug": True, "verbose": False}
    
flexible(1, 2, 3, name="test");
    
# Required: 1
    
# Extra positional: (2, 3)
    
# Extra keyword: {"name": "test"}
}

Unpacking arguments:

def add(a: int, b: int, c: int) -> int {
    
return a + b + c;
}

with entry {
    
# Unpack list/tuple into positional args
    
values = [1, 2, 3];
    
result = add(*values);  # add(1, 2, 3)

    
# Unpack dict into keyword args
    
params = {"a": 1, "b": 2, "c": 3};
    
result = add(**params);  # add(a=1, b=2, c=3)

    
# Combined unpacking
    
result = add(*[1, 2], **{"c": 3});  # add(1, 2, c=3)
}

4 can vs def#

Jac has two keywords for defining callable behavior: def for standard functions/methods and can for event-driven abilities on archetypes. Use def when you want explicit calling; use can when behavior should trigger automatically based on walker/node context.
Feature 	def 	can
Call style 	Called explicitly: obj.method() 	Triggered automatically on walker entry/exit
Used in 	Any archetype, standalone functions 	Walkers, nodes, edges
Syntax 	def name(args) -> Type { } 	can name with NodeType entry { }
Best for 	Regular methods, utility functions, API endpoints 	Graph traversal logic, event handlers

walker ListItems {
    
has items: list = [];

    
# 'can' ability -- fires automatically when walker enters a Root node
    
can collect with Root entry {
        
visit [-->];
    
}

    
# 'can' ability -- fires on each Item node visited
    
can gather with Item entry {
        
self.items.append(here.value);
    
}

    
# 'can' ability -- fires when walker exits Root
    
can report_all with Root exit {
        
report self.items;
    
}
}

    See Part III: OSP for complete walker and ability documentation.

5 Methods#

The def keyword declares methods on archetypes:

obj Calculator {
    
has total: float = 0.0;

    
def add(value: float) -> float {
        
self.total += value;
        
return self.total;
    
}

    
def reset() -> None {
        
self.total = 0.0;
    
}
}

6 Static Methods#

obj Counter {
    
static has count: int = 0;

    
# Static method
    
static def get_count() -> int {
        
return Counter.count;
    
}

    
# Instance method
    
def increment() -> None {
        
Counter.count += 1;
    
}
}

7 Lambda Expressions#

# Simple lambda (note spacing around type annotations)
glob add = lambda a: int , b: int -> int : a + b;

# Lambda with block
glob process = lambda x: int -> int {
    
result = x * 2;
    
result += 1;
    
return result;
};

# Lambda without parameters
glob get_value = lambda : 42;

# Lambda with return type only
glob get_default = lambda -> int : 100;

# Lambda with default parameters
glob power = lambda x: int = 2 , y: int = 3 : x ** y;

# Using lambdas
glob numbers = [1, 2, 3, 4, 5];
glob squared = list(map(lambda x: int : x ** 2, numbers));
glob evens = list(filter(lambda x: int : x % 2 == 0, numbers));

# Lambda returning lambda
glob make_adder = lambda x: int : (lambda y: int : x + y);
glob add_five = make_adder(5);  # add_five(10) returns 15

8 Immediately Invoked Function Expressions (IIFE)#

with entry {
    
result = (lambda x: int -> int: x * 2)(5);  # result = 10
}

9 Decorators#

def decorator(func: any) -> any {
    
return func;
}

def decorator_with_args(arg1: any, arg2: any) -> any {
    
return lambda func: any: func;
}

@decorator
def my_function -> None {
    
print("decorated");
}

@decorator_with_args("a", "b")
def another_function -> None {
    
print("decorated with args");
}

10 Access Modifiers#

# Public (default, accessible everywhere)
def:pub public_func -> None { }

# Private (accessible only within the module)
def:priv _private_func -> None { }

# Protected (accessible within module and subclasses)
def:protect _protected_func -> None { }

Try it: Functions complete example

Object-Oriented Programming#

Jac uses obj instead of class to define types (though class is also supported for Python compatibility). The key differences from Python: fields are declared with has at the top of the definition, methods use can instead of def, and there's no explicit __init__ -- the constructor is generated automatically from has declarations.
1 Objects (Classes)#

Objects are Jac's basic unit of data and behavior. Use obj for general-purpose types. For graph-based programming, use node, edge, or walker instead (see Part III: OSP).

obj Person {
    
has name: str;
    
has age: int;

    
def postinit() -> None {
        
# Called after the auto-generated init completes
        
print(f"Created {self.name}");
    
}

    
def greet() -> str {
        
return f"Hi, I'm {self.name}";
    
}
}

with entry {
    
# Usage
    
person = Person(name="Alice", age=30);
    
print(person.greet());
}

2 Inheritance#

obj Animal {
    
has name: str;

    
def speak() -> str {
        
return "";  # Base implementation
    
}
}

obj Dog(Animal) {
    
has breed: str = "Unknown";

    
override def speak() -> str {
        
return "Woof!";
    
}
}

obj Cat(Animal) {
    
override def speak() -> str {
        
return "Meow!";
    
}
}

# Multiple inheritance
obj Pet(Animal, Trackable) {
    
has owner: str;
}

3 Enumerations#

enum Color {
    
RED = "red",
    
GREEN = "green",
    
BLUE = "blue"
}

# With auto values
enum Status {
    
PENDING,
    
ACTIVE,
    
COMPLETED
}

with entry {
    
# Usage
    
color = Color.RED;
    
status = Status.ACTIVE;
    
print(f"Color: {color}, Status: {status}");
}

4 Enums with Inline Python#

enum HttpStatus {
    
OK = 200,
    
NOT_FOUND = 404

    
::py::
    
def is_success(self):
        
return 200 <= self.value < 300

    
@property
    
def message(self):
        
return {200: "OK", 404: "Not Found"}.get(self.value, "Unknown")
    
::py::
}

5 Properties and Encapsulation#

obj Account {
    
has:priv _balance: float = 0.0;

    
def get_balance() -> float {
        
return self._balance;
    
}

    
def deposit(amount: float) -> None {
        
if amount > 0 {
            
self._balance += amount;
        
}
    
}
}

Try it: Objects and Enums complete example

Implementations and Forward Declarations#

Jac separates interface (what an object has and can do) from implementation (how it does it). This separation enables cleaner architecture, easier testing, and better organization of large codebases. You declare the interface in one place and implement abilities in impl blocks -- even in separate files.
1 Forward Declarations#

Forward declarations let you reference a type before it's fully defined. This is essential for circular references (like User referencing Post and Post referencing User) and for organizing code across multiple files.

# Forward declarations
obj User;
obj Post;

# Now define with mutual references
obj User {
    
has name: str;
    
has posts: list[Post] = [];
}

obj Post {
    
has content: str;
    
has author: User;
}

2 Implementation Blocks#

The impl keyword attaches method bodies to declared abilities. This pattern keeps your interface clean and readable while moving implementation details elsewhere. It's particularly useful for large classes, for providing multiple implementations (like mock versions for testing), or for organizing abilities that span many lines.

# Interface (declaration)
obj Calculator {
    
has value: float = 0.0;

    
def add(x: float) -> float;
    
def multiply(x: float) -> float;
}

# Implementation
impl Calculator.add {
    
self.value += x;
    
return self.value;
}

impl Calculator.multiply {
    
self.value *= x;
    
return self.value;
}

3 Separate Implementation Files#

Convention: Use .impl.jac files for implementations.

calculator.jac:

obj Calculator {
    
has value: float = 0.0;
    
def add(x: float) -> float;
    
def multiply(x: float) -> float;
}

calculator.impl.jac:

impl Calculator.add {
    
self.value += x;
    
return self.value;
}

impl Calculator.multiply {
    
self.value *= x;
    
return self.value;
}

4 Variant Modules#

A single logical module can be split across variant files that target different execution contexts. Variant suffixes are .sv.jac (server), .cl.jac (client), and .na.jac (native). All files sharing the same base name are automatically discovered and compiled together.

Head module precedence: .jac > .sv.jac > .cl.jac > .na.jac. The highest-precedence file that exists on disk becomes the head module; all lower-precedence variants are attached as variant annexes. If no plain .jac file exists, the next available variant acts as head.

mymod/
├── mymod.jac            # Head module (declarations + entry)
├── mymod.sv.jac         # Server variant (extra server-only declarations)
├── mymod.cl.jac         # Client variant (extra client-only declarations)
├── mymod.impl.jac       # Head implementations (can also impl variant decls)
├── impl/
│   └── mymod.sv.impl.jac   # Server variant impl (from shared folder)
└── mymod.test.jac       # Tests

Each variant gets its own symbol table during parsing. The compiler then connects declarations and implementations across all variants:

    Impl files match their variant automatically (e.g., mymod.sv.impl.jac provides bodies for declarations in mymod.sv.jac).
    A head impl file (mymod.impl.jac) can provide implementations for declarations in any variant (cross-variant matching).
    Impl files can live in the same directory or in an impl/ subdirectory.

mymod.jac:

obj Circle {
    
has radius: float;
    
def area -> float;
}

mymod.sv.jac:

obj CircleService {
    
has name: str;
    
def describe -> str;
}

mymod.cl.jac:

obj Display {
    
has label: str;
    
def render -> str;
}

mymod.impl.jac (cross-variant -- provides impls for both head and client variant):

impl Circle.area -> float {
    
return 3.14159 * self.radius * self.radius;
}

impl Display.render -> str {
    
return "Displaying: " + self.label;
}

impl/mymod.sv.impl.jac (server variant impl from shared folder):

impl CircleService.describe -> str {
    
return "Service: " + self.name;
}

Native Variant Files (.na.jac)#

Native variant files compile to LLVM IR and execute via JIT (MCJIT). Code in .na.jac files runs as native machine code, bypassing the Python runtime entirely. This is useful for performance-critical code and for calling C libraries directly. The same functionality is available inside na {} blocks in regular .jac files.

C Library Imports:

Native code can import C shared libraries using the import from syntax with a library path and extern function declarations, either at the top level of a .na.jac file or inside a na {} block:

# math_native.na.jac
import from "/usr/lib/libm.so.6" {
    
def sqrt(x: f64) -> f64;
    
def pow(base: f64, exp: f64) -> f64;
}

def hypotenuse(a: f64, b: f64) -> f64 {
    
return sqrt(a * a + b * b);
}

Declarations inside the braces are body-less function signatures that become LLVM declare (extern) statements. The shared library is loaded automatically at JIT time, and symbols are resolved by name.

Type mapping: Jac's int maps to i64 and float maps to f64 in native code. Use fixed-width types (i8, i16, i32, u8, u16, u32, f32, etc.) when C functions expect specific sizes. The compiler automatically coerces between standard and fixed-width types at call boundaries.

Example -- calling raylib from Jac:

# game.na.jac
import from "libraylib.so" {
    
def InitWindow(width: i32, height: i32, title: str) -> None;
    
def CloseWindow() -> None;
    
def WindowShouldClose() -> i8;
    
def BeginDrawing() -> None;
    
def EndDrawing() -> None;
    
def ClearBackground(color: i32) -> None;
    
def DrawText(text: str, x: i32, y: i32, size: i32, color: i32) -> None;
}

with entry {
    
InitWindow(800, 600, "Hello from Jac");
    
while WindowShouldClose() == 0 {
        
BeginDrawing();
        
ClearBackground(0);
        
DrawText("Jac + Raylib", 300, 280, 30, -1);
        
EndDrawing();
    
}
    
CloseWindow();
}

5 When to Use Implementations#

    Circular dependencies: Forward declare to break cycles
    Code organization: Keep interfaces clean
    UI components: Separate render tree from method logic (.cl.jac + .impl.jac)
    Plugin architectures: Define interfaces that plugins implement
    Large codebases: Separate concerns across files
    Variant modules: Split server, client, and native code into separate files while keeping them as one logical module
    C interop: Use .na.jac files to call C libraries directly from JIT-compiled native code

Learn More#

Tutorials:

    Jac Basics - Objects, functions, and syntax
    Testing - Write tests for your code

Related Reference:

    Part I: Foundation - Variables, types, control flow
    Part III: OSP - Nodes, edges, walkers

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Object-Spatial Programming
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
            Foundation
            Primitives & Codespace Semantics
            Functions & Objects
            Object-Spatial Programming
            Concurrency
            Comprehensions & Filters
            Learn by Doing
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Introduction to OSP
        1 What is OSP?
        2 Why OSP?
        3 Core Concepts
        4 Complete Example
    Nodes
        1 Node Declaration
        2 Node Entry/Exit Abilities
        3 Node Inheritance
    Edges
        1 Edge Declaration
        2 Edge Entry/Exit
        3 Directed vs Undirected
    Walkers
        1 Walker Declaration
        2 Walker State
        3 The visit Statement
        4 The report Statement
        5 The disengage Statement
        6 Spawning Walkers
        When to Use Walkers vs Functions
        Walkers as REST APIs
        7 Walker Inheritance
        8 Special References
    Graph Construction
        1 Creating Nodes
        2 Creating Edges
        3 Chained Construction
        4 Deleting Nodes and Edges
            Cascade Deletion Pattern
        5 Built-in Graph Functions
    Graph Traversal
        1 Basic Traversal
        Traversal Semantics: Deferred Exits
        2 Filtered Traversal
        3 Entry and Exit Events
    Data Spatial Queries
        1 Edge Reference Syntax
        2 Attribute Filtering
        3 Complex Queries
    Typed Context Blocks
        1 What are Typed Context Blocks?
        2 Tuple-Based Dispatch
        3 Context Blocks in Nodes
        4 Complex Typed Context Example
    Common Walker Patterns
        CRUD Walker
        Search Walker
        Hierarchical Traversal
        Aggregate Walker
    Best Practices
    See Also

    Full Reference
    Language Specification

Part III: Object-Spatial Programming (OSP)#

In this part:

    Introduction to OSP - Concepts, motivation, core example
    Nodes - Node declaration, entry/exit abilities
    Edges - Edge declaration, typed connections
    Walkers - Walker declaration, visit, report, disengage
    Graph Construction - Creating and connecting nodes
    Graph Traversal - Filtered traversal, entry/exit events
    Data Spatial Queries - Edge references, attribute filtering
    Typed Context Blocks - Type-based dispatch

    Related Sections:

        Graph Operators - Connection and edge reference syntax
        Pipe Operators - Spawn traversal modes

Introduction to OSP#
1 What is OSP?#

Object-Spatial Programming models data as graphs and computation as mobile agents (walkers) that traverse the graph. Instead of calling functions on objects, walkers visit nodes and perform operations based on location.
2 Why OSP?#

    Natural graph modeling: Social networks, knowledge graphs, state machines
    AI agent architecture: Walkers are natural representations of AI agents
    Separation of concerns: Data (nodes/edges) separate from behavior (walkers)
    Spatial context: here, visitor provide natural context

3 Core Concepts#
Concept 	Description 	Keyword
Node 	Graph vertex holding data 	node
Edge 	Connection between nodes 	edge
Walker 	Mobile agent that traverses 	walker
Root 	Entry point to graph 	root
Here 	Walker's current location 	here
Visitor 	Reference to visiting walker 	visitor
4 Complete Example#

node Person {
    
has name: str;
    
has age: int;
}

edge Knows {
    
has since: int;
}

walker Greeter {
    
can greet with Root entry {
        
visit [-->];
    
}

    
can say_hello with Person entry {
        
print(f"Hello, {here.name}!");
        
visit [-->];
    
}
}

with entry {
    
# Build graph
    
alice = Person(name="Alice", age=30);
    
bob = Person(name="Bob", age=25);

    
root ++> alice;
    
alice +>: Knows(since=2020) :+> bob;

    
# Spawn walker
    
root spawn Greeter();
}

Nodes#

Nodes are the vertices of your graph -- they hold data and can have abilities that execute when walkers visit them. Think of nodes as "smart objects" that know when they're being visited and can react accordingly. Unlike regular objects, nodes can be connected via edges and participate in graph traversals.
1 Node Declaration#

node Person {
    
has name: str;
    
has age: int = 0;

    
can greet with Visitor entry {
        
print(f"Hello from {self.name}");
    
}
}

# Node with no data
node Waypoint { }

2 Node Entry/Exit Abilities#

Abilities triggered when walkers enter or exit. The event clause syntax is:

can ability_name with [TypeExpression] (entry | exit) { ... }

Where TypeExpression is optional - if omitted, the ability triggers for ALL walkers.

node SecureRoom {
    
has clearance_required: int;

    
# Generic entry - triggers for ANY walker (no type filter)
    
can on_enter with entry {
        
print("Someone entered");
    
}

    
# Typed entry - triggers only for Inspector walkers
    
can check_clearance with Inspector entry {
        
if visitor.clearance < self.clearance_required {
            
print("Access denied");
            
disengage;
        
}
    
}

    
# Type reference entry - using Root for root
    
can at_root with Root entry {
        
print("At root node");
    
}

    
# Walker exiting
    
can on_exit with Inspector exit {
        
print("Inspector leaving");
    
}

    
# Multiple walker types (union)
    
can process with Walker1 | Walker2 entry {
        
print("Processing for Walker1 or Walker2");
    
}
}

Event Clause Forms:
Form 	Triggers When
with entry 	Any walker enters (no type filter)
with TypeName entry 	Walker of TypeName enters
with Root entry 	At root node entry
with Type1 \| Type2 entry 	Walker of either type enters
with exit 	Any walker exits
with TypeName exit 	Walker of TypeName exits
3 Node Inheritance#

node Entity {
    
has id: str;
    
has created_at: str;
}

node User(Entity) {
    
has username: str;
    
has email: str;
}

Edges#

Edges are first-class connections between nodes. Unlike simple object references, edges can carry their own data (like relationship strength or timestamps) and have their own types. This lets you model rich relationships -- "Alice knows Bob since 2020" becomes natural to express. Use typed edges when the relationship itself has meaningful attributes.
1 Edge Declaration#

edge Friend {
    
has since: int;
    
has strength: float = 1.0;
}

edge Follows { }  # Edge with no data

edge Weighted {
    
has weight: float;

    
def get_normalized(max_weight: float) -> float {
        
return self.weight / max_weight;
    
}
}

2 Edge Entry/Exit#

Walkers can trigger abilities on edges during traversal:

edge Road {
    
has distance: float;

    
can on_traverse with Traveler entry {
        
visitor.total_distance += self.distance;
    
}
}

3 Directed vs Undirected#

Edge direction is determined by connection operators:

node Item {}

with entry {
    
a = Item();
    
b = Item();

    
a ++> b;          # Directed: a → b
    
a <++> b;         # Undirected: a ↔ b (creates edges both ways)
}

Walkers#

Walkers are mobile agents that traverse the graph, executing abilities at each node they visit. Unlike functions that you call, walkers go to data. They maintain state throughout their journey, making them ideal for tasks like collecting information across a graph, implementing AI agents that navigate knowledge structures, or processing pipelines where context accumulates. Spawn a walker with root spawn MyWalker() to begin traversal.
1 Walker Declaration#

walker Collector {
    
has items: list = [];
    
has max_items: int = 10;

    
can start with Root entry {
        
print("Starting collection");
        
visit [-->];
    
}

    
can collect with DataNode entry {
        
if len(self.items) < self.max_items {
            
self.items.append(here.value);
        
}
        
visit [-->];
    
}
}

2 Walker State#

Walkers maintain state throughout their traversal:

node DataNode {
    
has value: int;
}

walker Counter {
    
has count: int = 0;

    
can start with Root entry {
        
self.count += 1;
        
visit [-->];
    
}

    
can count_nodes with DataNode entry {
        
self.count += 1;
        
visit [-->];
    
}
}

with entry {
    
root ++> DataNode(value=1) ++> DataNode(value=2);
    
walker_instance = Counter();
    
root spawn walker_instance;
    
print(f"Counted {walker_instance.count} nodes");  # Output: 3
}

    Note: Walker abilities must specify which node types they handle. Use Root for the root node and specific node types for others. A generic with entry only triggers at the spawn location.

3 The visit Statement#

The visit statement tells the walker where to go next. It doesn't immediately move -- it queues nodes for the next step of traversal. This queue-based approach lets you control breadth-first vs depth-first traversal and handle cases where there's nowhere to go (using the else clause).

Traversal Must Be Explicit

Without a visit statement in an ability, the walker stops at the current node. If a walker visits root and then reaches a Person node but the Person ability has no visit [-->], the walker will not continue to the next person. Traversal must be explicitly requested at each step.

Basic Syntax:

node Item {}

walker Visitor {
    
can go with Item entry {
        
visit [-->];                    # Visit all outgoing nodes
        
visit [<--];                    # Visit all incoming nodes
        
visit [<-->];                   # Visit both directions
    
}
}

With Type Filters:

node Person {}
edge Friend { has since: int = 2020; }

walker Visitor {
    
can filter with Person entry {
        
visit [-->](?:Person);          # Visit Person nodes only
        
visit [->:Friend:->];           # Visit via Friend edges only
        
visit [->:Friend:since>2020:->]; # Via Friend edges with condition
    
}
}

With Else Clause:

node Item {}

walker Visitor {
    
can traverse with Item entry {
        
visit [-->] else {              # Fallback if no nodes to visit
            
print("No outgoing edges");
        
}
    
}
}

Direct Node Visit:

node Item {}

walker Visitor {
    
has target: Item | None = None;

    
can direct with Item entry {
        
visit here;                     # Visit current node
        
visit self.target;              # Visit node stored in walker field
    
}
}

Queue Insertion Index:

The visit : index : [-->] syntax controls where in the walker's traversal queue new destinations are inserted. This enables DFS, BFS, and custom traversal strategies:

node Item {}

walker Visitor {
    
can traverse with Item entry {
        
visit : 0 : [-->];              # Insert at FRONT of queue (DFS behavior)
        
visit : -1 : [-->];             # Insert at END of queue (BFS behavior)
        
visit : 2 : [-->];              # Insert at position 2 in queue
    
}
}

Syntax 	Queue Position 	Effect
visit [-->] 	End (default) 	BFS-like -- standard breadth-first traversal
visit : 0 : [-->] 	Front 	DFS-like -- depth-first by inserting at front
visit : -1 : [-->] 	End 	Explicit BFS -- same as default
visit : N : [-->] 	Position N 	Custom insertion point

Out-of-bounds indices fall back to appending at the end.
4 The report Statement#

Send data back without stopping:

node DataNode {
    
has value: int = 0;
}

walker DataCollector {
    
can start with Root entry {
        
visit [-->];
    
}

    
can collect with DataNode entry {
        
report here.value;  # Continues execution
        
visit [-->];
    
}
}

with entry {
    
root ++> DataNode(value=1);
    
result = root spawn DataCollector();
    
all_values = result.reports;  # List of reported values
}

5 The disengage Statement#

The disengage statement immediately terminates a walker's traversal. Use it when the walker has found what it was looking for (like a search hitting its target) or when a condition means further traversal would be pointless. It's the walker equivalent of return from a recursive function.

walker Searcher {
    
has target: str;

    
can search with Person entry {
        
if here.name == self.target {
            
report here;
            
disengage;  # Stop traversal
        
}
        
visit [-->];
    
}
}

6 Spawning Walkers#

node Item { has value: int = 0; }

walker MyWalker {
    
has param: int = 0;

    
can visit with Root entry {
        
visit [-->];
    
}
    
can collect with Item entry {
        
report here.value;
        
visit [-->];
    
}
}

with entry {
    
node1 = Item(value=1);
    
node2 = Item(value=2);
    
node3 = Item(value=3);
    
root ++> node1 ++> node2 ++> node3;

    
# Basic spawn
    
result = root spawn MyWalker();

    
# Spawn with parameters
    
result = root spawn MyWalker(param=10);

    
# Access results
    
print(result.reports);  # All reported values
}

When to Use Walkers vs Functions#

Jac provides two ways to expose server logic: def:pub functions and walker types. Choose based on your needs:
	def:pub Functions 	Walkers
Best for 	Simple stateless CRUD, quick prototyping 	Graph traversal, per-user data, production apps
Auth 	Shared data (no user isolation) 	Per-user root node (walker:priv enforces auth)
Data access 	Direct: [root -->] 	Traversal: visit [-->], here
API style 	Function call → HTTP endpoint 	Spawn walker at node
State 	Stateless 	Carries state across nodes via has properties

Rule of Thumb

Start with def:pub to prototype quickly. Switch to walkers when you need authentication, per-user data isolation, or multi-step graph traversal. The walker:priv visibility modifier automatically enforces that the walker runs on the authenticated user's private root node.
Walkers as REST APIs#

Public walkers automatically become HTTP endpoints when you run jac start:

node Todo {
    
has title: str;
    
has done: bool = False;
}

walker add_todo {
    
has title: str;

    
can create with Root entry {
        
new_todo = here ++> Todo(title=self.title);
        
report new_todo;
    
}
}

walker list_todos {
    
can list with Root entry {
        
for todo in [-->](?:Todo) {
            
report todo;
        
}
    
}
}

# Run as API server
jac
 start app.jac

# Call via HTTP
curl
 -X POST http://localhost:8000/walker/add_todo \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn OSP"}'

Walker has properties become the request body. The report values become the response. See Part IV: Full-Stack and jac-scale Reference for full API documentation.
7 Walker Inheritance#

walker BaseVisitor {
    
can log with entry {
        
print(f"Visiting: {here}");
    
}
}

walker DetailedVisitor(BaseVisitor) {
    
override can log with entry {
        
print(f"Detailed visit to: {type(here).__name__}");
    
}
}

8 Special References#

These keywords have special meaning in specific contexts:
Reference 	Valid Context 	Description 	See Also
self 	Any method/ability 	Current instance (walker, node, object) 	Part II: Functions
here 	Walker ability 	Current node the walker is visiting 	Walkers
visitor 	Node ability 	The walker that triggered this ability 	Nodes
root 	Anywhere 	Root node of the current graph 	Graph Construction
super 	Subclass method 	Parent class reference 	Part II
init 	Object body 	Constructor method name 	Part II
postinit 	Object body 	Post-constructor hook 	Part I
props 	JSX context 	Component props reference 	Part IV: Full-Stack

Usage examples:

node SecureRoom {
    
has required_level: int;

    
# 'visitor' refers to the walker visiting this node
    
# 'self' refers to this node instance
    
can check with Inspector entry {
        
if visitor.clearance >= self.required_level {
            
print("Access granted to " + visitor.name);
        
}
    
}
}

walker Inspector {
    
has clearance: int;
    
has name: str;

    
# 'here' refers to the current node being visited
    
# 'self' refers to this walker instance
    
can inspect with SecureRoom entry {
        
print(f"{self.name} inspecting room at {here}");
        
print(f"Room requires level {here.required_level}");
    
}

    
can start with Root entry {
        
# 'root' is always the graph root
        
print(f"Starting from root: {root}");
        
visit [-->];
    
}
}

When each reference is valid:
Context 	self 	here 	visitor 	root
Walker ability 	Walker instance 	Current node 	N/A 	Graph root
Node ability 	Node instance 	N/A 	Visiting walker 	Graph root
Object method 	Object instance 	N/A 	N/A 	Graph root
Free code 	N/A 	N/A 	N/A 	Graph root
Graph Construction#
1 Creating Nodes#

node Person {
    
has name: str;
    
has age: int;
}

with entry {
    
# Create and assign
    
alice = Person(name="Alice", age=30);
    
bob = Person(name="Bob", age=25);

    
# Inline creation in connection
    
root ++> Person(name="Charlie", age=35);
}

The ++> operator returns a list

The ++> operator returns a list containing the created node(s). Access the node with [0] index:

new_node = here ++> Todo(id="123", title="Buy groceries");
created_todo = new_node[0];  # Access the actual node
report created_todo;

2 Creating Edges#

node Person { has name: str; }
edge Friend { has since: int = 2020; }
edge Colleague { has department: str = ""; }

with entry {
    
alice = Person(name="Alice");
    
bob = Person(name="Bob");

    
# Untyped (generic edge)
    
alice ++> bob;

    
# Typed edge
    
alice +>: Friend(since=2020) :+> bob;

    
# Bidirectional typed
    
alice <+: Colleague(department="Engineering") :+> bob;
}

3 Chained Construction#

node Item {}
edge Start {}
edge Next {}
edge End {}

with entry {
    
a = Item();
    
b = Item();
    
c = Item();
    
d = Item();

    
# Build chains in one expression
    
root ++> a ++> b ++> c ++> d;

    
# With typed edges
    
root +>: Start :+> a +>: Next :+> b +>: Next :+> c +>: End :+> d;
}

4 Deleting Nodes and Edges#

node Person { has name: str; }
edge Friend {}

with entry {
    
alice = Person(name="Alice");
    
bob = Person(name="Bob");
    
alice +>: Friend :+> bob;

    
# Delete specific edge
    
alice del --> bob;

    
# Delete node
    
del bob;
}

# Delete current node from within a walker
walker Cleanup {
    
can check with Todo entry {
        
if here.completed {
            
node_id = here.id;
            
del here;
            
report {"deleted": node_id};
        
}
    
}
}

Cascade Deletion Pattern#

Delete a node and all its related nodes:

walker:priv DeleteWithChildren {
    
has parent_id: str;

    
can search with Root entry {
        
visit [-->];
    
}

    
can delete with Todo entry {
        
# Delete if this is the target or a child of the target
        
if here.id == self.parent_id or here.parent_id == self.parent_id {
            
del here;
        
}
    
}
}

5 Built-in Graph Functions#
Function 	Description
jid(node) 	Get unique Jac ID of object
jobj(node) 	Get Jac object wrapper
grant(node, user) 	Grant access permission
revoke(node, user) 	Revoke access permission
allroots() 	Get all root references
save(node) 	Persist node to storage
commit() 	Commit pending changes
printgraph(root) 	Print graph structure to stdout (output depends on graph size; may require logging configuration to see results)

node Person { has name: str; }

with entry {
    
alice = Person(name="Alice");
    
bob = Person(name="Bob");
    
secret_node = Person(name="Secret");

    
id = jid(alice);
    
save(alice);
    
printgraph(root);
}

Graph Traversal#
1 Basic Traversal#

Walker traversal is queue-based (BFS-like by default):

walker BFSWalker {
    
can start with Root entry {
        
print(f"Starting at: {here}");
        
visit [-->];
    
}

    
can traverse with Person entry {
        
print(f"Visiting: {here.name}");
        
visit [-->];  # Queue all outgoing for later visits
    
}
}

Traversal Semantics: Deferred Exits#

Walker traversal uses recursive post-order exit execution. Entry abilities execute immediately when entering a node, while exit abilities are deferred until all descendants are visited. This means exits execute in LIFO order (last visited node exits first), similar to function call stack unwinding.

node Step { has label: str; }

walker Logger {
    
can start with Root entry {
        
visit [-->];  # Begin traversal from root
    
}

    
can enter with Step entry {
        
print(f"ENTER: {here.label}");
        
visit [-->];
    
}

    
can leave with Step exit {
        
print(f"EXIT: {here.label}");
    
}
}

# Setup: root -> A -> B -> C
# root spawn Logger();
#
# Output:
#   ENTER: A
#   ENTER: B
#   ENTER: C
#   EXIT: C    ← innermost exits first
#   EXIT: B
#   EXIT: A    ← outermost exits last

This is useful for aggregation patterns where you need to collect results from children before processing the parent (e.g., calculating subtree totals, building trees bottom-up).
2 Filtered Traversal#

node Person { has age: int = 0; }
edge Friend { has since: int = 2020; }

walker FilteredWalker {
    
can start with Root entry {
        
visit [-->];  # Start traversal from root
    
}

    
can traverse with Person entry {
        
# By node type
        
visit [-->](?:Person);

        
# By edge type
        
visit [->:Friend:->];

        
# Combined: Friend edges to Person nodes since 2020
        
visit [->:Friend:since > 2020:->](?:Person);
    
}
}

3 Entry and Exit Events#

node Room {
    
can on_enter with Visitor entry {
        
print("Entering room");
    
}

    
can on_exit with Visitor exit {
        
print("Exiting room");
    
}
}

Data Spatial Queries#
1 Edge Reference Syntax#

node Person {}
edge EdgeType {}
edge Edge { has attr: int = 0; has a: int = 0; has b: int = 0; }
edge Friend {}

walker Traverser {
    
can query with Person entry {
        
# Basic forms
        
outgoing = [-->];                     # All outgoing nodes
        
incoming = [<--];                     # All incoming nodes
        
both = [<-->];                        # Both directions

        
# Typed forms
        
via_type = [->:EdgeType:->];          # Outgoing via EdgeType

        
# With conditions
        
filtered = [->:Edge:attr > 0:->];     # Filter by edge attribute

        
# Node type filter
        
people = [-->](?:Person);             # Filter result nodes by type

        
# Get edges vs nodes
        
edges = [edge -->];                   # Get edge objects
        
friends = [edge ->:Friend:->];        # Typed edge objects
    
}
}

Use [edge -->] when you need to access edge attributes or visit edges directly.
2 Attribute Filtering#

node User {
    
has age: int = 0;
    
has status: str = "";
    
has verified: bool = False;
}
edge Friend { has since: int = 2020; }
edge Link { has weight: float = 0.0; }

walker Filter {
    
can query with User entry {
        
# Filter by node attributes (after traversal)
        
adults = [-->](?age >= 18);
        
active = [-->](?status == "active");

        
# Filter by edge attributes (during traversal)
        
recent_friends = [->:Friend:since > 2020:->];
        
strong_connections = [->:Link:weight > 0.8:->];
    
}
}

3 Complex Queries#

node Person { has age: int = 0; }
edge Friend { has since: int = 2020; }
edge Colleague {}

walker Querier {
    
can complex with Person entry {
        
# Chained traversal (multi-hop)
        
friends_of_friends = [here ->:Friend:-> ->:Friend:->];

        
# Mixed edge types
        
path = [here ->:Friend:-> ->:Colleague:->];

        
# Combined with filters
        
target = [->:Friend:since < 2020:->](?:Person, age > 30);
    
}
}

Typed Context Blocks#
1 What are Typed Context Blocks?#

Typed context blocks let you conditionally execute code based on the runtime type of the current node. Instead of writing separate abilities for each node type, you can handle multiple types within a single ability using ->Type{code} blocks. This is especially useful when a walker visits a heterogeneous graph with different node types.

The syntax uses ->Type{code} with no space between the arrow and type name:

walker AnimalVisitor {
    
can visit with Animal entry {
        
# Typed context block for Dog (subtype of Animal)
        
->Dog{print(f"{here.name} is a {here.breed} dog");}

        
# Typed context block for Cat (subtype of Animal)
        
->Cat{print(f"{here.name} says meow");}

        
# Default case (any other Animal type)
        
->_{print(f"{here.name} is some animal");}
    
}
}

Syntax Notes:

    No space between -> and the type name: ->Dog{ not -> Dog {
    Opening brace immediately follows the type
    Code typically on same line with closing brace
    Use ->_ for default/catch-all case

2 Tuple-Based Dispatch#

walker Processor {
    
can process with (Node1, Node2) entry {
        
# Handle when visiting involves both types
    
}
}

3 Context Blocks in Nodes#

Nodes reacting to different walker types:

node DataNode {
    
has value: int;

    
can handle with Walker entry {
        
->Reader{print(f"Read value: {self.value}");}

        
->Writer{
            
self.value = visitor.new_value;
            
print(f"Updated to: {self.value}");
        
}
    
}
}

4 Complex Typed Context Example#

From the reference examples, showing inheritance-based dispatch:

walker ShoppingCart {
    
can process_item with Product entry {
        
print(f"Processing {type(here).__name__}...");

        
# Each subtype gets its own block
        
->Book{print(f"  -> Book: '{here.title}' by {here.author}");}
        
->Magazine{print(f"  -> Magazine: '{here.title}' Issue #{here.issue}");}
        
->Electronics{print(f"  -> Electronics: {here.name}, warranty {here.warranty_years}yr");}

        
self.total += here.price;
        
visit [-->];
    
}
}

Common Walker Patterns#
CRUD Walker#

# Create
walker:priv CreateItem {
    
has name: str;
    
can create with Root entry {
        
new_item = here ++> Item(name=self.name);
        
report new_item[0];
    
}
}

# Read (List)
walker:priv ListItems {
    
has items: list = [];
    
can collect with Root entry { visit [-->]; }
    
can gather with Item entry { self.items.append(here); }
    
can finish with Root exit { report self.items; }
}

# Update
walker:priv UpdateItem {
    
has item_id: str;
    
has new_name: str;
    
can find with Root entry { visit [-->]; }
    
can update with Item entry {
        
if here.id == self.item_id {
            
here.name = self.new_name;
            
report here;
        
}
    
}
}

# Delete
walker:priv DeleteItem {
    
has item_id: str;
    
can find with Root entry { visit [-->]; }
    
can remove with Item entry {
        
if here.id == self.item_id {
            
del here;
            
report {"deleted": self.item_id};
        
}
    
}
}

Search Walker#

node Item {
    
has id: str;
    
has name: str;
}

def calculate_relevance(item: Item, query: str) -> int {
    
return 1;
}

walker:priv SearchItems {
    
has query: str;
    
has matches: list = [];

    
can start with Root entry {
        
visit [-->];
    
}

    
can check with Item entry {
        
if self.query.lower() in here.name.lower() {
            
self.matches.append({
                
"id": here.id,
                
"name": here.name,
                
"score": calculate_relevance(here, self.query)
            
});
        
}
    
}

    
can finish with Root exit {
        
self.matches.sort(key=lambda x: any: x["score"], reverse=True);
        
report self.matches;
    
}
}

Hierarchical Traversal#

walker:priv GetTree {
    def build_tree(node: any) -> dict {
        children = [];
        for child in [node -->] {
            children.append(self.build_tree(child));
        }
        return {
            "id": node.id,
            "name": node.name,
            "children": children
        };
    }

    can start with Root entry {
        tree = self.build_tree(here);
        report tree;
    }
}

Aggregate Walker#

walker:priv GetStats {
    
has total: int = 0;
    
has completed: int = 0;

    
can count with Root entry {
        
visit [-->];
    
}

    
can tally with Todo entry {
        
self.total += 1;
        
if here.completed {
            
self.completed += 1;
        
}
    
}

    
can summarize with Root exit {
        
report {
            
"total": self.total,
            
"completed": self.completed,
            
"pending": self.total - self.completed,
            
"completion_rate": (self.completed / self.total * 100) if self.total > 0 else 0
        
};
    
}
}

Best Practices#

    Use specific entry points -- with Todo entry is more efficient than generic with entry
    Accumulate then report -- Collect data during traversal, report once at exit
    Handle empty graphs -- Always check if traversal found anything
    Use meaningful node types -- Makes code self-documenting
    Keep walkers focused -- One walker, one responsibility

See Also#

    Walker Responses - Patterns for handling .reports array
    Build an AI Day Planner - Full-stack tutorial using OSP concepts
    OSP Tutorial - Hands-on tutorial with exercises
    What Makes Jac Different - Gentle introduction to Jac's core concepts

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Concurrency
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
            Foundation
            Primitives & Codespace Semantics
            Functions & Objects
            Object-Spatial Programming
            Concurrency
            Comprehensions & Filters
            Learn by Doing
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Async/Await
        1 Async Functions
        2 Async Walkers
        3 Async For Loops
    Concurrent Expressions
        1 flow Keyword
        2 Parallel Operations
        3 flow vs async
    Learn More

    Full Reference
    Language Specification

Part VI: Concurrency#

In this part:

    Async/Await - Async functions, async walkers, async for
    Concurrent Expressions - flow/wait for parallel tasks

Jac supports Python-style async/await for concurrent I/O operations, plus a unique flow/wait syntax for launching and collecting parallel tasks. Use async when you need non-blocking I/O (like HTTP requests), and flow when you want to run multiple independent operations concurrently.
Async/Await#

Note

Async functions must be awaited in an async context. In with entry blocks, use await directly or wrap calls in an async ability.

The async/await syntax works like Python's -- async marks a function as a coroutine, and await suspends execution until the awaited operation completes. Walkers can also be async, enabling non-blocking graph traversal with I/O at each node.
1 Async Functions#

async def fetch_data(url: str) -> dict {
    
response = await http_get(url);
    
return await response.json();
}

async def process_multiple(urls: list[str]) -> list[dict] {
    
results = [];
    
for url in urls {
        
data = await fetch_data(url);
        
results.append(data);
    
}
    
return results;
}

2 Async Walkers#

async walker DataFetcher {
    
has url: str;

    
async can fetch with Root entry {
        
data = await http_get(self.url);
        
report data;
    
}
}

Use async walker for non-blocking I/O during traversal.
3 Async For Loops#

async def process_stream(stream: AsyncIterator) -> None {
    
async for item in stream {
        
print(item);
    
}
}

Concurrent Expressions#

The flow/wait pattern provides explicit concurrency control. flow launches a task and immediately returns a future (without blocking), while wait retrieves the result (blocking if necessary). This is more explicit than async/await -- you decide exactly when to start parallel work and when to synchronize.
1 flow Keyword#

The flow keyword launches a function call as a background task and returns a future immediately. Use it when you have independent operations that can run in parallel.

def expensive_computation -> int {
    
return 42;
}

def do_something_else -> int {
    
return 1;
}

with entry {
    
future = flow expensive_computation();

    
# Do other work while computation runs
    
other_result = do_something_else();

    
# Wait for result when needed
    
result = wait future;
}

2 Parallel Operations#

def fetch_users -> list {
    
return [];
}

def fetch_orders -> list {
    
return [];
}

def fetch_inventory -> list {
    
return [];
}

def process_local_data {
    
# Process local data here
}

with entry {
    
# Launch multiple operations in parallel
    
future1 = flow fetch_users();
    
future2 = flow fetch_orders();
    
future3 = flow fetch_inventory();

    
# Continue with other work
    
process_local_data();

    
# Collect all results
    
users = wait future1;
    
orders = wait future2;
    
inventory = wait future3;
}

3 flow vs async#
Feature 	async/await 	flow/wait
Model 	Event loop (cooperative) 	Thread pool (parallel)
Best for 	I/O-bound, many concurrent 	CPU-bound, few concurrent
Blocking 	Non-blocking 	Can block threads
Learn More#

Related Reference:

    Part I: Foundation - Control flow basics
    Part V: AI Integration - Async LLM calls

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Comprehensions & Filters
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
            Foundation
            Primitives & Codespace Semantics
            Functions & Objects
            Object-Spatial Programming
            Concurrency
            Comprehensions & Filters
            Learn by Doing
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Standard Comprehensions
    Filter Comprehensions
    Typed Filter Comprehensions
    Assign Comprehensions

    Full Reference
    Language Specification

Comprehensions & Filters#

In this part:

    Standard Comprehensions - List, dict, set, generator
    Filter Comprehensions - The ? operator on collections
    Typed Filter Comprehensions - Filter by type with ?:Type
    Assign Comprehensions - Bulk update with =

Jac extends Python's comprehension syntax with filter (?) and assign (=) operators that work on collections of nodes or objects. These provide concise ways to query and modify groups of items.

    Related:

        Error Handling - Try/except/finally, raising exceptions
        Pipe Operators - Forward/backward pipes
        Testing - Test blocks, assertions, CLI commands

Standard Comprehensions#

def example() {
    
# List comprehension
    
squares = [x ** 2 for x in range(10)];

    
# With condition
    
evens = [x for x in range(20) if x % 2 == 0];

    
# Dict comprehension
    
squared_dict = {x: x ** 2 for x in range(5)};

    
# Set comprehension
    
strings = ["hello", "world", "hi"];
    
unique_lengths = {len(s) for s in strings};

    
# Generator expression
    
gen = (x ** 2 for x in range(1000000));
}

Filter Comprehensions#

Filter collections with ?condition:

node Person {
    
has age: int,
        
status: str;
}

node Employee {
    
has salary: int,
        
experience: int;
}

def example(people: list[Person], employees: list[Employee]) {
    
# Filter people by age
    
adults = people(?age >= 18);

    
# Multiple conditions
    
qualified = employees(?salary > 50000, experience >= 5);

    
# On graph traversal results
    
friends = [-->](?status == "active");
}

Typed Filter Comprehensions#

Filter by type with filter syntax:

node Dog {
    
has name: str;
}

node Cat {
    
has indoor: bool;
}

node Person {
    
has age: int;
}

def example(animals: list) {
    
dogs = animals(?:Dog);                    # By type only
    
indoor_cats = animals(?:Cat, indoor==True); # Type with condition
    
people = [-->](?:Person);                 # On graph traversal
    
adults = [-->](?:Person, age > 21);        # Traversal with condition
}

Assign Comprehensions#

Modify all items with =attr=value:

node Person {
    
has age: int,
        
verified: bool = False,
        
can_vote: bool = False;
}

node Item {
    
has status: str,
        
processed_at: str;
}

def now() -> str {
    
return "2024-01-01";
}

def example(people: list[Person], items: list[Item]) {
    
# Set attribute on all items
    
people(=verified=True);

    
# Chained: filter then assign
    
people(?age >= 18)(=can_vote=True);

    
# Multiple assignments
    
items(=status="processed", processed_at=now());
}

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
byLLM Reference
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
            byLLM Reference
            Learn by Doing
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Meaning Typed Programming
        The Concept
        Implicit vs Explicit Semantics
        Type Validation
    Installation
    Model Configuration
        Default (Zero-Config)
        Custom Model (Override)
        Model Constructor Parameters
        Supported Providers
    Project Configuration
        Default Model Configuration
        System Prompt Override
        HTTP Client for Custom Endpoints
    Core Syntax
        Function Declaration
        Method Declaration
        Inline Expression
    Return Types
        Primitive Types
        Enum Types
        Object Types
        List Types
        Optional Types
    Invocation Parameters
        Examples
    Semantic Strings (semstrings)
        Parameter Semantics
        Complex Semantic Types
    Tool Calling (ReAct)
        Defining Tools
        Using Tools
        Method Tools
    Streaming
    Multimodal Inputs
        Image Type
            Supported Input Formats
            In-Memory Usage
        Structured Output from Images
        Video Type
            Video Parameters
            Structured Output from Videos
        Multimodal with Tools
        Python Multimodal Integration
    Context Methods
        incl_info
        Object Context
    Python Integration
    Best Practices
        1. Descriptive Names and sem for Clarity
        2. Descriptive Parameters
        3. Semantic Strings for Complex Types
        4. Tool Semantics
        5. Limit Tool Count
    Error Handling
    Testing with MockLLM
    Complex Structured Output Example
    LiteLLM Proxy Server
        Setup
        Parameters
    Creating Custom Model Classes
        Implementation
        Usage
        Required Methods
    Advanced Python Integration
        Mode 1: Direct Python Import
        Mode 2: Implement in Jac, Import to Python (Recommended)
        Semstrings in Python
        Hyperparameters in Python
        Tools in Python
    Agentic AI Patterns
        AI Agents as Walkers
        Tool-Using Agents
        Context Injection with incl_info
        Agentic Walkers
        Multi-Agent Systems
    Related Resources

    Full Reference
    AI Integration

byLLM Reference#

Complete reference for byLLM, the AI integration framework implementing Meaning-Typed Programming (MTP).
Meaning Typed Programming#

Meaning Typed Programming (MTP) is Jac's core AI paradigm. Your function signature -- the name, parameter names, and types -- becomes the specification. The LLM reads this "meaning" and generates appropriate behavior. This works because well-named functions already describe their intent; MTP just makes that intent executable.
The Concept#

MTP treats semantic intent as a first-class type. You declare what you want, and AI provides how:

# The function signature IS the specification
def classify_sentiment(text: str) -> str by llm;

# Usage - the LLM infers behavior from the name and types
with entry {
    
result = classify_sentiment("I love this product!");
    
# result = "positive"
}

Implicit vs Explicit Semantics#

Implicit -- derived from function/parameter names:

def translate_to_spanish(text: str) -> str by llm;

Explicit -- using sem for detailed descriptions:

sem classify = """
Analyze the emotional tone of the input text.
Return exactly one of: 'positive', 'negative', 'neutral'.
Consider context and sarcasm.
""";

def classify(text: str) -> str by llm;

Type Validation#

byLLM validates that LLM responses match the declared return type. If the LLM returns an invalid type, byLLM will:

    Attempt coercion -- e.g., string "5" becomes integer 5
    Raise an error if coercion fails

This means your Jac type system functions as the LLM's output schema. Declaring -> int guarantees you receive an integer, and declaring -> MyObj guarantees you receive a properly structured object.
Installation#

pip
 install byllm

For video support, install with the video extra:

pip
 install byllm[video]

Model Configuration#
Default (Zero-Config)#

llm is a built-in name in Jac -- just use by llm() directly with no imports:

def summarize(text: str) -> str by llm();

with entry {
    
print(summarize("Jac is a programming language..."));
}

The default model is gpt-4o-mini. Configure it via jac.toml (see Default Model Configuration below).
Custom Model (Override)#

For per-file customization, override the builtin with an explicit Model:

import from byllm.lib { Model }

glob llm = Model(model_name="gpt-4o");

Model Constructor Parameters#
Parameter 	Type 	Required 	Description
model_name 	str 	Yes 	Model identifier (e.g., "gpt-4o", "claude-3-5-sonnet-20240620")
api_key 	str 	No 	API key for the model provider (defaults to environment variable)
config 	dict 	No 	Configuration dictionary (see below)

Config Dictionary Options:
Key 	Type 	Description
base_url 	str 	Custom API endpoint URL (aliases: host, api_base)
proxy 	bool 	Enable proxy mode (uses OpenAI client with base_url)
http_client 	bool 	Enable direct HTTP requests (for custom endpoints)
ca_bundle 	str/bool 	SSL certificate path, True for default, False to skip verification
api_key 	str 	API key (alternative to constructor parameter)
verbose 	bool 	Enable verbose/debug logging
outputs 	list 	Mock responses for MockLLM testing

Example with config:

glob llm = Model(
    
model_name="gpt-4o",
    
config={
        
"base_url": "https://your-endpoint.com/v1",
        
"proxy": True
    
}
);

Supported Providers#

byLLM uses LiteLLM for model integration, providing access to 100+ providers.
OpenAI
Anthropic
Google Gemini
Ollama (Local)
HuggingFace

[plugins.byllm.model]
default_model = "gpt-4o"

export OPENAI_API_KEY="sk-..."

You can also override per-file with glob llm = Model(...) (see Custom Model (Override)).

Provider Model Name Formats:
Provider 	Model Name Format 	Example
OpenAI 	gpt-* 	gpt-4o, gpt-4o-mini
Anthropic 	claude-* 	claude-3-5-sonnet-20240620
Google 	gemini/* 	gemini/gemini-2.0-flash
Ollama 	ollama/* 	ollama/llama3:70b
HuggingFace 	huggingface/* 	huggingface/meta-llama/Llama-3.3-70B-Instruct
Full Provider List

Project Configuration#
Default Model Configuration#

The builtin llm is configured via jac.toml. This controls the model used by any by llm() call that doesn't explicitly override llm:

[plugins.byllm.model]
default_model = "gpt-4o-mini"    # Model to use (any LiteLLM-supported model)
api_key = ""                      # API key (env vars take precedence)
base_url = ""                     # Custom API endpoint URL
proxy = false                     # Enable proxy mode (uses OpenAI client)
verbose = false                   # Log LLM calls to stderr

[plugins.byllm.call_params]
temperature = 0.7                 # Model creativity (0.0-2.0)
max_tokens = 0                    # Max response tokens (0 = no limit)

[plugins.byllm.litellm]
local_cost_map = true             # Use local cost map
drop_params = true                # Drop unsupported params per provider

[plugins.byllm.model] options:
Key 	Type 	Default 	Description
default_model 	str 	"gpt-4o-mini" 	LiteLLM model identifier (e.g. "gpt-4o", "claude-sonnet-4-6", "gemini/gemini-2.0-flash")
api_key 	str 	"" 	API key for the provider. Environment variables (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.) take precedence
base_url 	str 	"" 	Custom API endpoint URL (for proxy or self-hosted models)
proxy 	bool 	false 	Enable proxy mode (uses OpenAI client instead of LiteLLM)
verbose 	bool 	false 	Log LLM calls and parameters to stderr

[plugins.byllm.call_params] options:
Key 	Type 	Default 	Description
temperature 	float 	0.7 	Creativity/randomness (0.0-2.0, lower is more deterministic)
max_tokens 	int 	0 	Maximum response tokens (0 = no limit / model default)

[plugins.byllm.litellm] options:
Key 	Type 	Default 	Description
local_cost_map 	bool 	true 	Use local cost map instead of fetching from remote
drop_params 	bool 	true 	Silently drop parameters unsupported by the chosen provider

Minimal setup -- just set your API key and go:

export OPENAI_API_KEY="sk-..."

# No imports needed -- llm is a builtin
def greet(name: str) -> str by llm();

with entry {
    
print(greet("Alice"));
}

System Prompt Override#

Override the default system prompt globally via jac.toml:

[plugins.byllm]
system_prompt = "You are a helpful assistant that provides concise answers."

The system prompt is automatically applied to all by llm() function calls, providing:

    Centralized control over LLM behavior across your project
    Consistent personality without repeating prompts in code
    Easy updates without touching source code

HTTP Client for Custom Endpoints#

For custom or self-hosted models, configure HTTP client in the Model constructor:

import from byllm.lib { Model }

glob llm = Model(
    
model_name="custom-model",
    
config={
        
"api_base": "https://your-endpoint.com/v1/chat/completions",
        
"api_key": "your_api_key_here",
        
"http_client": True,
        
"ca_bundle": True  # True (default SSL), False (skip), or "/path/to/cert.pem"
    
}
);

HTTP Client Options:
Parameter 	Type 	Description
api_base 	str 	Full URL to your chat completions endpoint
api_key 	str 	Bearer token for authentication
http_client 	bool 	Enable direct HTTP mode (bypasses LiteLLM)
ca_bundle 	bool/str 	SSL certificate verification
Core Syntax#
Function Declaration#

# Basic function
def function_name(param: type) -> return_type by llm();

# With sem for additional context (recommended for ambiguous names)
def function_name(param: type) -> return_type by llm();
sem function_name = "Description of what the function does.";

Method Declaration#

obj MyClass {
    
has attribute: str;

    
# Method has access to self attributes
    
def method_name() -> str by llm();
}

Inline Expression#

Not Yet Implemented

The inline by llm expression syntax is planned but not yet available. Use a function declaration instead:

# Instead of: response = "prompt" by llm;
# Use:
def explain(topic: str) -> str by llm();

with entry {
    
response = explain("quantum computing");
}

Return Types#
Primitive Types#

def get_summary(text: str) -> str by llm();
def count_words(text: str) -> int by llm();
def is_positive(text: str) -> bool by llm();
def get_score(text: str) -> float by llm();

Enum Types#

enum Sentiment {
    
POSITIVE,
    
NEGATIVE,
    
NEUTRAL
}

def analyze_sentiment(text: str) -> Sentiment by llm();

Enum member semstrings are included in the LLM's schema, helping the model understand what each value means:

enum Personality {
    
INTROVERT,
    
EXTROVERT,
    
AMBIVERT
}

sem Personality.INTROVERT = "Prefers solitude and small groups, energized by alone time";
sem Personality.EXTROVERT = "Thrives in social settings, energized by interaction";
sem Personality.AMBIVERT = "Comfortable in both social and solitary settings";

def classify_personality(bio: str) -> Personality by llm();

Object Types#

obj Person {
    
has name: str;
    
has age: int;
    
has bio: str | None;
}

def extract_person(text: str) -> Person by llm();

List Types#

def extract_keywords(text: str) -> list[str] by llm();
def find_people(text: str) -> list[Person] by llm();

Optional Types#

def find_date(text: str) -> str | None by llm();

Invocation Parameters#

Parameters passed to by llm() at call time:
Parameter 	Type 	Description
temperature 	float 	Controls randomness (0.0 = deterministic, 2.0 = creative). Default: 0.7
max_tokens 	int 	Maximum tokens in response
tools 	list 	Tool functions for agentic behavior (automatically enables ReAct loop)
incl_info 	dict 	Additional context key-value pairs injected into the prompt
stream 	bool 	Enable streaming output (only supports str return type)
max_react_iterations 	int 	Maximum ReAct iterations before forcing final answer

Deprecated: method parameter

The method parameter ("ReAct", "Reason", "Chain-of-Thoughts") is deprecated and was never functional. The ReAct tool-calling loop is automatically enabled when tools=[...] is provided. Simply pass tools directly instead of method="ReAct".
Examples#

# With temperature control
# Note: Max temperature varies by provider (Anthropic: 0.0-1.0, OpenAI: 0.0-2.0)
def generate_story(prompt: str) -> str by llm(temperature=0.9);
def extract_facts(text: str) -> str by llm(temperature=0.0);

# With max tokens
def summarize(text: str) -> str by llm(max_tokens=100);

# With tools (enables ReAct loop)
def calculate(expression: str) -> float by llm(tools=[add, multiply]);

# With additional context
def personalized_greeting(name: str) -> str by llm(
    
incl_info={"current_time": get_time(), "location": "NYC"}
);

# With streaming
def generate_essay(topic: str) -> str by llm(stream=True);

Semantic Strings (semstrings)#

The sem keyword attaches semantic descriptions to functions, parameters, type fields, and enum values. These strings are included in the compiler-generated prompt so the LLM sees them at runtime.

Best practice

Always use sem to provide context for by llm() functions and parameters. Docstrings are for human documentation (and auto-generated API docs) but are not included in compiler-generated prompts. Only sem declarations affect LLM behavior.

obj Customer {
    
has id: str;
    
has name: str;
    
has tier: str;
}

# Object-level semantic
sem Customer = "A customer record in the CRM system";

# Attribute-level semantics
sem Customer.id = "Unique customer identifier (UUID format)";
sem Customer.name = "Full legal name of the customer";
sem Customer.tier = "Service tier: 'basic', 'premium', or 'enterprise'";

# Enum value semantics
enum Priority { LOW, MEDIUM, HIGH }
sem Priority.HIGH = "Urgent: requires immediate attention";

Parameter Semantics#

sem analyze_code.code = "The source code to analyze";
sem analyze_code.language = "Programming language (python, javascript, etc.)";
sem analyze_code.return = "A structured analysis with issues and suggestions";

def analyze_code(code: str, language: str) -> dict by llm;

Complex Semantic Types#

obj CodeAnalysis {
    
has issues: list[str];
    
has suggestions: list[str];
    
has complexity_score: int;
    
has summary: str;
}

sem analyze.return = """
Return a CodeAnalysis object with:
- issues: List of problems found
- suggestions: Improvement recommendations
- complexity_score: 1-10 complexity rating
- summary: One paragraph overview
""";

def analyze(code: str) -> CodeAnalysis by llm;

Tool Calling (ReAct)#
Defining Tools#

"""Get the current date in YYYY-MM-DD format."""
def get_date() -> str {
    
import from datetime { datetime }
    
return datetime.now().strftime("%Y-%m-%d");
}

"""Search the database for matching records."""
def search_db(query: str, limit: int = 10) -> list[dict] {
    
# Implementation
    
return results;
}

"""Send an email notification."""
def send_email(to: str, subject: str, body: str) -> bool {
    
# Implementation
    
return True;
}

Using Tools#

def answer_question(question: str) -> str by llm(
    
tools=[get_date, search_db, send_email]
);

Method Tools#

obj Calculator {
    
has memory: float = 0;

    
def add(x: float) -> float {
        
self.memory += x;
        
return self.memory;
    
}

    
def clear() -> float {
        
self.memory = 0;
        
return self.memory;
    
}

    
def calculate(instructions: str) -> str by llm(
        
tools=[self.add, self.clear]
    
);
}

Streaming#

For real-time token output:

def generate_story(topic: str) -> str by llm(stream=True);

with entry {
    
for token in generate_story("space exploration") {
        
print(token, end="", flush=True);
    
}
    
print();
}

Limitations:

    Only supports str return type
    Tool calling not supported in streaming mode

Multimodal Inputs#

byLLM supports image and video inputs through the Image and Video types. These can be used as parameters in any by llm() function or method.
Image Type#

Import and use the Image type for image inputs:

import from byllm.lib { Image }

"""Describe what you see in this image."""
def describe_image(img: Image) -> str by llm();

with entry {
    
image = Image("photo.jpg");
    
description = describe_image(image);
    
print(description);
}

Supported Input Formats#

The Image constructor accepts multiple formats:
Format 	Example
File path 	Image("photo.jpg")
URL (http/https) 	Image("https://example.com/image.png")
Google Cloud Storage 	Image("gs://bucket/path/image.png")
Data URL 	Image("data:image/png;base64,...")
PIL Image 	Image(pil_image)
Bytes 	Image(raw_bytes)
BytesIO 	Image(bytes_io_buffer)
pathlib.Path 	Image(Path("photo.jpg"))
In-Memory Usage#

import from byllm.lib { Image }
import io;
import from PIL { Image as PILImage }

with entry {
    
pil_img = PILImage.open("photo.jpg");

    
# From BytesIO buffer
    
buf = io.BytesIO();
    
pil_img.save(buf, format="PNG");
    
img_from_buffer = Image(buf);

    
# From raw bytes
    
img_from_bytes = Image(buf.getvalue());

    
# From PIL image directly
    
img_from_pil = Image(pil_img);
}

Structured Output from Images#

Image inputs combine with all return types -- primitives, enums, objects, and lists:

import from byllm.lib { Image }

obj LineItem {
    
has description: str;
    
has quantity: int;
    
has price: float;
}

obj Receipt {
    
has store_name: str;
    
has date: str;
    
has items: list[LineItem];
    
has total: float;
}

"""Extract all information from this receipt image."""
def parse_receipt(img: Image) -> Receipt by llm();

with entry {
    
receipt = parse_receipt(Image("receipt.jpg"));
    
print(f"Store: {receipt.store_name}");
    
for item in receipt.items {
        
print(f"  - {item.description}: ${item.price}");
    
}
    
print(f"Total: ${receipt.total}");
}

Video Type#

The Video type processes videos by extracting frames at a configurable rate:

import from byllm.lib { Video }

"""Describe what happens in this video."""
def explain_video(video: Video) -> str by llm();

with entry {
    
video = Video(path="sample_video.mp4", fps=1);
    
explanation = explain_video(video);
    
print(explanation);
}

Video requires extra dependency

Video support requires pip install byllm[video].
Video Parameters#
Parameter 	Type 	Default 	Description
path 	str 	required 	Path to the video file
fps 	int 	1 	Frames per second to extract

Lower fps values extract fewer frames, reducing token usage. Higher values provide more temporal detail.
Structured Output from Videos#

import from byllm.lib { Video }

obj VideoAnalysis {
    
has summary: str;
    
has key_events: list[str];
    
has duration_estimate: str;
    
has content_type: str;
}

"""Analyze this video and extract key information."""
def analyze_video(video: Video) -> VideoAnalysis by llm();

Multimodal with Tools#

Image and video inputs work with tool calling:

import from byllm.lib { Image }

"""Search for products matching the description."""
def search_products(query: str) -> list[str] {
    
return [f"Product matching '{query}' - $29.99"];
}

"""Look at the image and find similar products."""
def find_similar_products(img: Image) -> str by llm(
    
tools=[search_products]
);

with entry {
    
results = find_similar_products(Image("shoe.jpg"));
    
print(results);
}

Python Multimodal Integration#

Multimodal works in both Python integration modes:

import jaclang
from byllm.lib import Model, Image, by

llm = Model(model_name="gpt-4o")

@by(llm)
def describe(img: Image) -> str: ...

img = Image("photo.jpg")
print(describe(img))

For a step-by-step walkthrough, see the Multimodal AI Tutorial.
Context Methods#
incl_info#

Pass additional context to the LLM:

obj User {
    
has name: str;
    
has preferences: dict;

    
def get_recommendation() -> str by llm(
        
incl_info={
            
"current_time": datetime.now().isoformat(),
            
"weather": get_weather(),
            
"trending": get_trending_topics()
        
}
    
);
}

Object Context#

Methods automatically include object attributes:

obj Article {
    
has title: str;
    
has content: str;
    
has author: str;

    
# LLM sees title, content, and author
    
def generate_summary() -> str by llm();
    
def suggest_tags() -> list[str] by llm();
}

Python Integration#

byLLM works in Python with the @by decorator:

from byllm.lib import Model, by
from dataclasses import dataclass
from enum import Enum

llm = Model(model_name="gpt-4o")

@by(llm)
def translate(text: str, language: str) -> str:  ...

class Sentiment(Enum):
    
POSITIVE = "positive"
    
NEGATIVE = "negative"
    
NEUTRAL = "neutral"

@by(llm)
def analyze(text: str) -> Sentiment: ...

@dataclass
class Person:
    
name: str
    
age: int

@by(llm)
def extract_person(text: str) -> Person: ...

Best Practices#
1. Descriptive Names and sem for Clarity#

# Good - name is self-explanatory
def extract_emails(text: str) -> list[str] by llm();

# Better - sem adds detail when needed
def extract_emails(text: str) -> list[str] by llm();
sem extract_emails = "Extract all email addresses from the text. Return empty list if none found.";

2. Descriptive Parameters#

# Good
def translate(source_text: str, target_language: str) -> str by llm();

# Avoid
def translate(t: str, l: str) -> str by llm();

3. Semantic Strings for Complex Types#

obj Order {
    
has id: str;
    
has status: str;
    
has items: list[dict];
}

sem Order.status = "Order status: 'pending', 'processing', 'shipped', 'delivered', 'cancelled'";
sem Order.items = "List of items with 'sku', 'quantity', and 'price' fields";

4. Tool Semantics#

Use sem to describe tools so the LLM knows when to call them:

sem search_products = "Search products in the catalog and return matching records.";
sem search_products.query = "Search terms";
sem search_products.category = "Optional category filter";
sem search_products.max_results = "Maximum number of results (default 10)";
def search_products(query: str, category: str = "", max_results: int = 10) -> list[dict] {
    
# Implementation
}

5. Limit Tool Count#

Too many tools can confuse the LLM. Keep to 5-10 relevant tools per function.
Error Handling#

with entry {
    
try {
        
result = my_llm_function(input);
    
} except Exception as e {
        
print(f"LLM error: {e}");
        
# Fallback logic
    
}
}

Testing with MockLLM#

Use MockLLM for deterministic testing without API calls. Mock responses are returned sequentially from the outputs list:

import from byllm.lib { MockLLM }

glob llm = MockLLM(
    
model_name="mockllm",
    
config={
        
"outputs": ["Mocked response 1", "Mocked response 2"]
    
}
);

def translate(text: str) -> str by llm();
def summarize(text: str) -> str by llm();

test "translate returns first mock" {
    
result = translate("Hello");
    
assert result == "Mocked response 1";
}

test "summarize returns second mock" {
    
result = summarize("Long text...");
    
assert result == "Mocked response 2";
}

MockLLM is useful for:

    Unit testing LLM-powered functions without API costs
    Deterministic assertions on function behavior
    CI/CD pipelines where API keys aren't available

Complex Structured Output Example#

byLLM validates that responses match the declared return type, coercing when possible (e.g., "5" → 5) and raising errors when coercion fails. This enables deeply nested structured outputs:
Resume Parser

LiteLLM Proxy Server#

byLLM can connect to a LiteLLM proxy server for enterprise deployments. This allows centralized model management, rate limiting, and cost tracking.
Setup#

    Deploy LiteLLM proxy following the official documentation

    Connect byLLM to the proxy:

import from byllm.lib { Model }

glob llm = Model(
    
model_name="gpt-4o",
    
api_key="your_litellm_virtual_key",
    
config={"api_base": "http://localhost:8000"}
);

from byllm.lib import Model

llm = Model(
    
model_name="gpt-4o",
    
api_key="your_litellm_virtual_key",
    
config={"api_base": "http://localhost:8000"}
)

Parameters#
Parameter 	Description
model_name 	The model to use (must be configured in LiteLLM proxy)
api_key 	LiteLLM virtual key or master key (not the provider API key)
config 	Configuration dict; set api_base to the URL of your LiteLLM proxy server (also accepts base_url or host as aliases)

For virtual key generation, see LiteLLM Virtual Keys.
Creating Custom Model Classes#

For self-hosted models or custom APIs not supported by LiteLLM, create a custom model class by inheriting from BaseLLM.
Implementation#
Python
Jac

from byllm.llm import BaseLLM
from openai import OpenAI

class MyCustomModel(BaseLLM):
    
def __init__(self, model_name: str, **kwargs) -> None:
        """Initialize the custom model."""
        
super().__init__(model_name, **kwargs)

    
def model_call_no_stream(self, params):
        """Handle non-streaming calls."""
        
client = OpenAI(api_key=self.api_key)
        
response = client.chat.completions.create(**params)
        
return response

    
def model_call_with_stream(self, params):
        """Handle streaming calls."""
        
client = OpenAI(api_key=self.api_key)
        
response = client.chat.completions.create(stream=True, **params)
        
return response

Usage#

glob llm = MyCustomModel(model_name="my-custom-model");

def generate(prompt: str) -> str by llm();

Required Methods#
Method 	Description
model_call_no_stream(params) 	Handle standard (non-streaming) LLM calls
model_call_with_stream(params) 	Handle streaming LLM calls

The params dictionary contains the formatted request including messages, model name, and any additional parameters.
Advanced Python Integration#

byLLM provides two modes for Python integration:
Mode 1: Direct Python Import#

Import byLLM directly in Python using the @by decorator:

import jaclang
from dataclasses import dataclass
from byllm.lib import Model, Image, by

llm = Model(model_name="gpt-4o")

@dataclass
class Person:
    
full_name: str
    
description: str
    
year_of_birth: int

@by(llm)
def get_person_info(img: Image) -> Person: ...

# Usage
img = Image("photo.jpg")
person = get_person_info(img)
print(f"Name: {person.full_name}")

Mode 2: Implement in Jac, Import to Python (Recommended)#

Implement AI features in Jac and import seamlessly into Python:
ai.jac
main.py

import from byllm.lib { Image }

obj Person {
    
has full_name: str;
    
has description: str;
    
has year_of_birth: int;
}

sem Person.description = "Short biography";

def get_person_info(img: Image) -> Person by llm();
sem get_person_info = "Extract person information from the image.";

Semstrings in Python#

Use the @Jac.sem decorator for semantic strings in Python:

from jaclang import JacRuntimeInterface as Jac
from dataclasses import dataclass
from byllm.lib import Model, by

llm = Model(model_name="gpt-4o")

@Jac.sem("Represents a personal record", {
    
"name": "Full legal name",
    
"dob": "Date of birth (YYYY-MM-DD)",
    
"ssn": "Last four digits of Social Security Number"
})
@dataclass
class Person:
    
name: str
    
dob: str
    
ssn: str

@by(llm)
def check_eligibility(person: Person, service: str) -> bool: ...

Hyperparameters in Python#

@by(llm(temperature=0.3, max_tokens=100))
def generate_joke() -> str: ...

Tools in Python#

def get_weather(city: str) -> str:
    
return f"The weather in {city} is sunny."

@by(llm(tools=[get_weather]))
def answer_question(question: str) -> str: ...

Agentic AI Patterns#
AI Agents as Walkers#

Combine graph traversal with LLM reasoning by using walkers as AI agents:

walker AIAgent {
    
has goal: str;
    
has memory: list = [];

    
can decide with Node entry {
        
context = f"Goal: {self.goal}\nCurrent: {here}\nMemory: {self.memory}";
        
decision = context by llm("Decide next action");
        
self.memory.append({"location": here, "decision": decision});
        
visit [-->];
    
}
}

Tool-Using Agents#

Agents combine LLM reasoning with tool functions. The LLM decides which tools to call and in what order (ReAct loop):

import from byllm.lib { Model }

glob llm = Model(model_name="gpt-4o");

glob kb: dict = {
    
"products": ["Widget A", "Widget B", "Service X"],
    
"prices": {"Widget A": 99, "Widget B": 149, "Service X": 29},
    
"inventory": {"Widget A": 50, "Widget B": 0, "Service X": 999}
};

"""List all available products."""
def list_products() -> list[str] {
    
return kb["products"];
}

"""Get the price of a product."""
def get_price(product: str) -> str {
    
if product in kb["prices"] {
        
return f"${kb['prices'][product]}";
    
}
    
return "Product not found";
}

"""Check if a product is in stock."""
def check_inventory(product: str) -> str {
    
qty = kb["inventory"].get(product, 0);
    
return f"In stock ({qty} available)" if qty > 0 else "Out of stock";
}

def sales_agent(request: str) -> str by llm(
    
tools=[list_products, get_price, check_inventory]
);
sem sales_agent = "Help customers browse products, check prices and availability.";

Context Injection with incl_info#

Pass additional runtime context to the LLM without modifying function signatures:

glob company_info = """
Company: TechCorp
Products: CloudDB, SecureAuth, DataViz
Support Hours: 9 AM - 5 PM EST
""";

def support_agent(question: str) -> str by llm(
    
incl_info={"company_context": company_info}
);
sem support_agent = "Answer customer questions about our products and services.";

The incl_info dict keys and values are injected into the prompt as additional context. This is useful for dynamic information that changes between calls.
Agentic Walkers#

Walkers that traverse document graphs and use LLM for analysis:

node Document {
    
has title: str;
    
has content: str;
    
has summary: str = "";
}

def summarize(content: str) -> str by llm();
sem summarize = "Summarize this document in 2-3 sentences.";

walker DocumentAgent {
    
has query: str;

    
can process with Root entry {
        
all_docs = [-->](?:Document);

        
for doc in all_docs {
            
if self.query.lower() in doc.content.lower() {
                
doc.summary = summarize(doc.content);
                
report {"title": doc.title, "summary": doc.summary};
            
}
        
}
    
}
}

Multi-Agent Systems#

Orchestrate multiple specialized walkers:

walker Coordinator {
    
can coordinate with Root entry {
        
research = root spawn Researcher(topic="AI");
        
writer = root spawn Writer(style="technical");
        
reviewer = root spawn Reviewer();

        
report {
            
"research": research.reports,
            
"draft": writer.reports,
            
"review": reviewer.reports
        
};
    
}
}

Related Resources#

    byLLM Quickstart Tutorial
    Structured Outputs Tutorial
    Agentic AI Tutorial
    Multimodal AI Tutorial
    MTP Research Paper
    LiteLLM Documentation

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
jac-client Reference
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
            jac-client Reference
            Learn by Doing
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Installation
    Project Setup
        Create New Project
        Project Structure
        The .cl.jac Convention
    Module System
        Import Statements
        Include Statements
        Export and Visibility
    Server-Side Development
        Server Code Blocks
        REST API with jac start
        Module Introspection
    Client Blocks
        Single-Statement Forms
        Export Requirement
    Components
        Function Components
        Using Props
        Composition
    Reactive State
        The has Keyword
        How It Works
        Complex State
    React Hooks
        useEffect (Automatic)
        useEffect (Manual)
        useContext
        Custom Hooks
    Backend Integration
        Calling Walkers from Client
        Walker Response
        Spawn Syntax
        Mutations (Create, Update, Delete)
        Error Handling Pattern
        Polling for Real-Time Updates
    Routing
        File-Based Routing (Recommended)
        Manual Routes
        URL Parameters
        Programmatic Navigation
        Nested Routes with Outlet
        Routing Hooks Reference
    Authentication
        Available Functions
        jacLogin
        jacSignup
        jacLogout / jacIsLoggedIn
        Per-User Graph Isolation
        Single Sign-On (SSO)
        AuthGuard for Protected Routes
    Styling
        Inline Styles
        CSS Classes
        CSS Files
        cn() Utility (Tailwind/shadcn)
        JSX Syntax Reference
    TypeScript Integration
    Configuration
        jac.toml
        NPM Registry Configuration
        Import Path Aliases
    CLI Commands
        Quick Reference
        jac build
        jac setup
        Extended Core Commands
    Multi-Target Architecture
        Web Target (Default)
        Desktop Target (Tauri)
        PWA Target
    Automatic Endpoint Caching
    BrowserRouter (Clean URLs)
    Build Error Diagnostics
    Build-Time Constants
    Development Server
        Prerequisites
        Start Server
        API Proxy
    Event Handlers
    Conditional Rendering
    Error Handling
        JacClientErrorBoundary
        Quick Start
        Built-in Wrapping
        Props
        Example with Custom Fallback
        Nested Boundaries
        Use Cases
    Memory & Persistence
        Memory Hierarchy
        TieredMemory
        ExecutionContext
        Anchor Management
    Development Tools
        Hot Module Replacement (HMR)
        Debug Mode
    Related Resources

    Full Reference
    Full-Stack Development

jac-client Reference#

Complete reference for jac-client, the full-stack web development plugin for Jac.
Installation#

pip
 install jac-client

Project Setup#
Create New Project#

jac
 create myapp --use client
cd myapp

Project Structure#

myapp/
├── jac.toml           # Project configuration
├── main.jac           # Entry point with app() function
├── components/        # Reusable components
│   └── Button.tsx     # TypeScript components supported
└── styles/            # CSS files
    └── main.css

The .cl.jac Convention#

Files ending in .cl.jac are automatically treated as client-side code -- no cl { } wrapper needed:

# components/Header.cl.jac -- automatically client-side
def:pub Header() -> JsxElement {
    
return <header>My App</header>;
}

This is equivalent to wrapping the contents in cl { } in a regular .jac file.
Module System#

Jac's module system bridges Python and JavaScript ecosystems. You can import from PyPI packages on the server and npm packages on the client using familiar syntax. The include statement (like C's #include) merges code directly, which is useful for splitting large files.
Import Statements#

# Simple import
import math;
import sys, json;

# Aliased import
import datetime as dt;

# From import
import from typing { List, Dict, Optional }
import from math { sqrt, pi, log as logarithm }

# Relative imports
import from . { sibling_module }
import from .. { parent_module }
import from .utils { helper_function }

# npm package imports (client-side)
import from react { useState, useEffect }
import from "@mui/material" { Button, TextField }

# CSS and asset imports
import "./styles.css";
import "./global.css";

Include Statements#

Include merges code directly (like C's #include):

include utils;  # Merges utils.jac into current scope

Export and Visibility#

# Public by default
def helper -> int { return 42; }

# Explicitly public
def:pub api_function -> None { }

# Private to module
def:priv internal_helper -> None { }

# Public walker (becomes API endpoint with jac start)
walker:pub GetUsers { }

# Private walker
walker:priv InternalProcess { }

Server-Side Development#
Server Code Blocks#

sv {
    
# Server-only block
    
node User {
        
has id: str;
        
has email: str;
    
}
}

# Single-statement form (no braces)
sv import from .database { connect_db }
sv node SecretData { has value: str; }

REST API with jac start#

Public walkers automatically become REST endpoints:

walker:pub GetUsers {
    
can get with Root entry {
        
users = [-->](?:User);
        
report users;
    
}
}

# Endpoint: POST /walker/GetUsers

Start the server:

jac
 start main.jac --port 8000

Module Introspection#

with entry {
    
# List all walkers in module
    
walkers = get_module_walkers();

    
# List all functions
    
functions = get_module_functions();
}

Client Blocks#

Use cl { } to define client-side (React) code:

cl {
    
def:pub app() -> JsxElement {
        
return <div>
            <h1>Hello, World!</h1>
        </div>;
    
}
}

Single-Statement Forms#

For one-off client-side declarations, use the single-statement cl prefix:

cl import from react { useState }
cl glob THEME: str = "dark";

Export Requirement#

The entry app() function must be exported with :pub:

cl {
    
def:pub app() -> JsxElement {  # :pub required
        
return <App />;
    
}
}

Components#
Function Components#

cl {
    
def:pub Button(props: dict) -> JsxElement {
        
return <button
            className={props.get("className", "")}
            onClick={props.get("onClick")}
        >
            {props.children}
        </button>;
    
}
}

Using Props#

cl {
    
def:pub Card(props: dict) -> JsxElement {
        
return <div className="card">
            <h2>{props["title"]}</h2>
            <p>{props["description"]}</p>
            {props.children}
        </div>;
    
}
}

Composition#

cl {
    
def:pub app() -> JsxElement {
        
return <div>
            <Card title="Welcome" description="Hello!">
                <Button onClick={lambda -> None { print("clicked"); }}>
                    Click Me
                </Button>
            </Card>
        </div>;
    
}
}

Reactive State#
The has Keyword#

Inside cl { } blocks, has creates reactive state:

cl {
    
def:pub Counter() -> JsxElement {
        
has count: int = 0;  # Compiles to useState(0)

        
return <div>
            <p>Count: {count}</p>
            <button onClick={lambda -> None { count = count + 1; }}>
                Increment
            </button>
        </div>;
    
}
}

How It Works#
Jac Syntax 	React Equivalent
has count: int = 0 	const [count, setCount] = useState(0)
count = count + 1 	setCount(count + 1)
Complex State#

cl {
    
def:pub Form() -> JsxElement {
        
has name: str = "";
        
has items: list = [];
        
has data: dict = {"key": "value"};

        
# Create new references for lists/objects
        
def add_item(item: str) -> None {
            
items = items + [item];  # Concatenate to new list
        
}

        
return <div>Form</div>;
    
}
}

Immutable Updates for Lists and Objects

State updates must produce new references to trigger re-renders. Mutating in place will not work.

# Correct - creates new list
todos = todos + [new_item];
todos = [t for t in todos if t["id"] != target_id];

# Wrong - mutates in place (no re-render)
todos.append(new_item);

React Hooks#
useEffect (Automatic)#

Similar to how has variables automatically generate useState, the can with entry and can with exit syntax automatically generates useEffect hooks:
Jac Syntax 	React Equivalent
can with entry { ... } 	useEffect(() => { ... }, [])
async can with entry { ... } 	useEffect(() => { (async () => { ... })(); }, [])
can with exit { ... } 	useEffect(() => { return () => { ... }; }, [])
can with [dep] entry { ... } 	useEffect(() => { ... }, [dep])
can with (a, b) entry { ... } 	useEffect(() => { ... }, [a, b])

cl {
    
def:pub DataLoader() -> JsxElement {
        
has data: list = [];
        
has loading: bool = True;

        
# Run once on mount (async with IIFE wrapping)
        
async can with entry {
            
data = await fetch_data();
            
loading = False;
        
}

        
# Cleanup on unmount
        
can with exit {
            
cleanup_subscriptions();
        
}

        
return <div>...</div>;
    
}

    
def:pub UserProfile(userId: str) -> JsxElement {
        
has user: dict = {};

        
# Re-run when userId changes (dependency array)
        
async can with [userId] entry {
            
user = await fetch_user(userId);
        
}

        
# Multiple dependencies using tuple syntax
        
async can with (userId, refresh) entry {
            
user = await fetch_user(userId);
        
}

        
return <div>{user.name}</div>;
    
}
}

useEffect (Manual)#

You can also use useEffect manually by importing it from React:

cl {
    
import from react { useEffect }

    
def:pub DataLoader() -> JsxElement {
        
has data: list = [];
        
has loading: bool = True;

        
# Run once on mount
        
useEffect(lambda -> None {
            
fetch_data();
        
}, []);

        
# Run when dependency changes
        
useEffect(lambda -> None {
            
refresh_data();
        
}, [some_dep]);

        
return <div>...</div>;
    
}
}

useContext#

cl {
    
import from react { createContext, useContext }

    
glob AppContext = createContext(None);

    
def:pub AppProvider(props: dict) -> JsxElement {
        
has theme: str = "light";

        
return <AppContext.Provider value={{"theme": theme}}>
            {props.children}
        </AppContext.Provider>;
    
}

    
def:pub ThemedComponent() -> JsxElement {
        
ctx = useContext(AppContext);
        
return <div className={ctx.theme}>Content</div>;
    
}
}

Custom Hooks#

Create reusable state logic by defining functions that use has:

cl {
    
import from react { useEffect }

    
def use_local_storage(key: str, initial_value: any) -> tuple {
        
has value: any = initial_value;

        
useEffect(lambda -> None {
            
stored = localStorage.getItem(key);
            
if stored {
                
value = JSON.parse(stored);
            
}
        
}, []);

        
useEffect(lambda -> None {
            
localStorage.setItem(key, JSON.stringify(value));
        
}, [value]);

        
return (value, lambda v: any -> None { value = v; });
    
}

    
def:pub Settings() -> JsxElement {
        
(theme, set_theme) = use_local_storage("theme", "light");
        
return <div>
            <p>Current: {theme}</p>
            <button onClick={lambda -> None { set_theme("dark"); }}>Dark</button>
        </div>;
    
}
}

Backend Integration#
Calling Walkers from Client#

Use native Jac spawn syntax to call walkers from client code. First, import your walkers with sv import, then spawn them:

# Import walkers from backend
sv import from ...main { get_tasks, create_task }

cl {
    
def:pub TaskList() -> JsxElement {
        
has tasks: list = [];
        
has loading: bool = True;

        
# Fetch data on component mount
        
async can with entry {
            
result = root spawn get_tasks();
            
if result.reports and result.reports.length > 0 {
                
tasks = result.reports[0];
            
}
            
loading = False;
        
}

        
if loading {
            
return <p>Loading...</p>;
        
}

        
return <ul>
            {[<li key={task["id"]}>{task["title"]}</li> for task in tasks]}
        
</ul>;
    
}
}

Walker Response#

The spawn call returns a result object:
Property 	Type 	Description
result.reports 	list 	Data reported by walker via report
result.status 	int 	HTTP status code
Spawn Syntax#
Syntax 	Description
root spawn WalkerName() 	Spawn walker from root node
root spawn WalkerName(arg=value) 	Spawn with parameters
node_id spawn WalkerName() 	Spawn from specific node

The spawn call returns a result object with:

    result.reports - Data reported by the walker
    result.status - HTTP status code

Mutations (Create, Update, Delete)#

sv import from ...main { add_task, toggle_task, delete_task }

cl {
    
def:pub TaskManager() -> JsxElement {
        
has tasks: list = [];

        
# Create
        
async def handle_add(title: str) -> None {
            
result = root spawn add_task(title=title);
            
if result.reports and result.reports.length > 0 {
                
tasks = tasks + [result.reports[0]];
            
}
        
}

        
# Update
        
async def handle_toggle(task_id: str) -> None {
            
result = root spawn toggle_task(task_id=task_id);
            
if result.reports and result.reports[0]["success"] {
                
tasks = [
                    
{**t, "completed": not t["completed"]} if t["id"] == task_id else t
                    
for t in tasks
                
];
            
}
        
}

        
# Delete
        
async def handle_delete(task_id: str) -> None {
            
result = root spawn delete_task(task_id=task_id);
            
if result.reports and result.reports[0]["success"] {
                
tasks = [t for t in tasks if t["id"] != task_id];
            
}
        
}

        
return <div>...</div>;
    
}
}

Error Handling Pattern#

Wrap spawn calls in try/catch and track loading/error state:

cl {
    
def:pub SafeDataView() -> JsxElement {
        
has data: any = None;
        
has loading: bool = True;
        
has error: str = "";

        
async can with entry {
            
loading = True;
            
try {
                
result = root spawn get_data();
                
if result.reports and result.reports.length > 0 {
                    
data = result.reports[0];
                
}
            
} except Exception as e {
                
error = f"Failed to load: {e}";
            
}
            
loading = False;
        
}

        
if loading { return <p>Loading...</p>; }
        
if error {
            
return <div>
                <p>{error}</p>
                <button onClick={lambda -> None { location.reload(); }}>Retry</button>
            </div>;
        
}
        
return <div>{JSON.stringify(data)}</div>;
    
}
}

Polling for Real-Time Updates#

Use setInterval with effect cleanup for periodic data refresh:

cl {
    
import from react { useEffect }

    
def:pub LiveData() -> JsxElement {
        
has data: any = None;

        
async def fetch_data() -> None {
            
result = root spawn get_live_data();
            
if result.reports and result.reports.length > 0 {
                
data = result.reports[0];
            
}
        
}

        
async can with entry { await fetch_data(); }

        
useEffect(lambda -> None {
            
interval = setInterval(lambda -> None { fetch_data(); }, 5000);
            
return lambda -> None { clearInterval(interval); };
        
}, []);

        
return <div>{data and <p>Last updated: {data["timestamp"]}</p>}</div>;
    
}
}

Routing#
File-Based Routing (Recommended)#

jac-client supports file-based routing using a pages/ directory:

myapp/
├── main.jac
└── pages/
    ├── index.jac          # /
    ├── about.jac          # /about
    ├── users/
    │   ├── index.jac      # /users
    │   └── [id].jac       # /users/:id (dynamic route)
    └── (auth)/            # Route group (parentheses)
        ├── layout.jac     # Shared layout for auth routes
        ├── login.jac      # /login
        └── signup.jac     # /signup

Route mapping:
File 	Route 	Description
pages/index.jac 	/ 	Home page
pages/about.jac 	/about 	Static page
pages/users/index.jac 	/users 	Users list
pages/users/[id].jac 	/users/:id 	Dynamic parameter
pages/[...notFound].jac 	* 	Catch-all (404)
pages/(auth)/dashboard.jac 	/dashboard 	Route group (no URL segment)
pages/layout.jac 	-- 	Wraps child routes with <Outlet />

Each page file exports a page function:

# pages/users/[id].jac
cl import from "@jac/runtime" { useParams, Link }

cl {
    
def:pub page() -> JsxElement {
        
params = useParams();
        
return <div>
            <Link to="/users">Back</Link>
            <h1>User {params.id}</h1>
        </div>;
    
}
}

Route groups organize pages without affecting the URL. A layout file can wrap them with authentication:

# pages/(auth)/layout.jac -- protects all pages in this group
cl import from "@jac/runtime" { AuthGuard, Outlet }

cl {
    
def:pub layout() -> JsxElement {
        
return <AuthGuard redirect="/login">
            <Outlet />
        </AuthGuard>;
    
}
}

Manual Routes#

For manual routing, import components from @jac/runtime:

cl import from "@jac/runtime" { Router, Routes, Route, Link }

cl {
    
def:pub app() -> JsxElement {
        
return <Router>
            <nav>
                <Link to="/">Home</Link>
                <Link to="/about">About</Link>
            </nav>

            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
            </Routes>
        </Router>;
    
}
}

URL Parameters#

cl import from "@jac/runtime" { useParams }

cl {
    
def:pub UserProfile() -> JsxElement {
        
params = useParams();
        
user_id = params["id"];

        
return <div>User: {user_id}</div>;
    
}

    
# Route: /user/:id
}

Programmatic Navigation#

cl import from "@jac/runtime" { useNavigate }

cl {
    
def:pub LoginForm() -> JsxElement {
        
navigate = useNavigate();

        
async def handle_login() -> None {
            
success = await do_login();
            
if success {
                
navigate("/dashboard");
            
}
        
}

        
return <button onClick={lambda -> None { handle_login(); }}>
            Login
        </button>;
    
}
}

Nested Routes with Outlet#

cl import from "@jac/runtime" { Outlet }

# pages/layout.jac -- root layout wrapping all pages
cl {
    
def:pub layout() -> JsxElement {
        
return <>
            <nav>...</nav>
            <main><Outlet /></main>
            <footer>...</footer>
        </>;
    
}
}

# pages/dashboard/layout.jac -- nested dashboard layout
cl {
    
def:pub DashboardLayout() -> JsxElement {
        
# Child routes render where Outlet is placed
        
return <div>
            <Sidebar />
            <main>
                <Outlet />
            </main>
        </div>;
    
}
}

Routing Hooks Reference#

Import from @jac/runtime:
Hook 	Returns 	Usage
useParams() 	dict 	Access URL parameters: params.id
useNavigate() 	function 	Navigate programmatically: navigate("/path"), navigate(-1)
useLocation() 	object 	Current location: location.pathname, location.search
Link 	component 	Navigation: <Link to="/path">Text</Link>
Outlet 	component 	Render child routes in layouts
AuthGuard 	component 	Protect routes: <AuthGuard redirect="/login">
Authentication#

jac-client provides built-in authentication functions via @jac/runtime.
Available Functions#
Function 	Returns 	Description
jacLogin(username, password) 	bool 	Login user, returns True on success
jacSignup(username, password) 	dict 	Register user, returns {success: bool, error?: str}
jacLogout() 	void 	Clear auth token
jacIsLoggedIn() 	bool 	Check if user is authenticated

Additional user management operations (available via API endpoints when using jac-scale):
Operation 	Description
Update Username 	Change username via API endpoint
Update Password 	Change password via API endpoint
Guest Access 	Anonymous user support via __guest__ account
jacLogin#

cl import from "@jac/runtime" { jacLogin, useNavigate }

cl {
    
def:pub LoginForm() -> any {
        
has username: str = "";
        
has password: str = "";
        
has error: str = "";

        
navigate = useNavigate();

        
async def handleLogin(e: any) -> None {
            
e.preventDefault();
            
# jacLogin returns bool (True = success, False = failure)
            
success = await jacLogin(username, password);
            
if success {
                
navigate("/dashboard");
            
} else {
                
error = "Invalid credentials";
            
}
        
}

        
return <form onSubmit={handleLogin}>...</form>;
    
}
}

jacSignup#

cl import from "@jac/runtime" { jacSignup }

cl {
    
async def handleSignup() -> None {
        
# jacSignup returns dict with success key
        
result = await jacSignup(username, password);
        
if result["success"] {
            
# User registered and logged in
            
navigate("/dashboard");
        
} else {
            
error = result["error"] or "Signup failed";
        
}
    
}
}

jacLogout / jacIsLoggedIn#

cl import from "@jac/runtime" { jacLogout, jacIsLoggedIn }

cl {
    
def:pub NavBar() -> any {
        
isLoggedIn = jacIsLoggedIn();

        
def handleLogout() -> None {
            
jacLogout();
            
# Redirect to login
        
}

        
return <nav>
            {isLoggedIn and (
                
<button onClick={lambda -> None { handleLogout(); }}>Logout</button>
            
) or (
                
<a href="/login">Login</a>
            
)}
        
</nav>;
    
}
}

Per-User Graph Isolation#

Each authenticated user gets an isolated root node:

walker:pub GetMyData {
    
can get with Root entry {
        
# 'root' is user-specific
        
my_data = [-->](?:MyData);
        
report my_data;
    
}
}

Single Sign-On (SSO)#

Configure in jac.toml:

[plugins.scale.sso.google]
client_id = "your-google-client-id"
client_secret = "your-google-client-secret"

SSO Endpoints:
Endpoint 	Description
/sso/{platform}/login 	Initiate SSO login
/sso/{platform}/register 	Initiate SSO registration
/sso/{platform}/login/callback 	OAuth callback
AuthGuard for Protected Routes#

Use AuthGuard to protect routes in file-based routing:

cl import from "@jac/runtime" { AuthGuard, Outlet }

# pages/(auth)/layout.jac
cl {
    
def:pub layout() -> any {
        
return <AuthGuard redirect="/login">
            <Outlet />
        </AuthGuard>;
    
}
}

Styling#
Inline Styles#

cl {
    
def:pub StyledComponent() -> JsxElement {
        
return <div style={{"color": "blue", "padding": "10px"}}>
            Styled content
        </div>;
    
}
}

CSS Classes#

cl {
    
def:pub Card() -> JsxElement {
        
return <div className="card card-primary">
            Content
        </div>;
    
}
}

CSS Files#

/* styles/main.css */
.card {
    padding: 1rem;
    border-radius: 8px;
}

cl {
    
import "./styles/main.css";
}

cn() Utility (Tailwind/shadcn)#

cl {
    
# cn() from local lib/utils.ts (shadcn/ui pattern)
    
import from "../lib/utils" { cn }

    
def:pub StylingExamples() -> JsxElement {
        
has condition: bool = True;
        
has hasError: bool = False;
        
has isSuccess: bool = True;

        
className = cn(
            
"base-class",
            
condition and "active",
            
{"error": hasError, "success": isSuccess}
        
);

        
return <div>
            <div className="p-4 bg-blue-500 text-white">Tailwind</div>
            <div className={className}>Dynamic</div>
        </div>;
    
}
}

    Note: The cn() utility is a local file you create in your project (shadcn/ui pattern):

    // lib/utils.ts
    import { type ClassValue, clsx } from "clsx"
    import { twMerge } from "tailwind-merge"
    export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }

JSX Syntax Reference#

cl {
    
def:pub JsxExamples() -> JsxElement {
        
has variable: str = "text";
        
has condition: bool = True;
        
has items: list = [];
        
has props: dict = {};

        
return <div>
            <input type="text" value={variable} />

            {condition and <div>Shown if true</div>}

            {items}

            <button {...props}>Click</button>
        </div>;
    
}
}

TypeScript Integration#

TypeScript/TSX files are automatically supported:

// components/Button.tsx
import React from 'react';

interface ButtonProps {
    label: string;
    onClick: () => void;
}

export const Button: React.FC<ButtonProps> = ({ label, onClick }) => {
    return <button onClick={onClick}>{label}</button>;
};

cl {
    
import from "./components/Button" { Button }

    
def:pub app() -> JsxElement {
        
return <Button label="Click" onClick={lambda -> None { }} />;
    
}
}

Configuration#
jac.toml#

[project]
name = "myapp"
version = "0.1.0"

[serve]
base_route_app = "app"        # Serve at /
cl_route_prefix = "/cl"       # Client route prefix

[plugins.client]
enabled = true

# Import path aliases
[plugins.client.paths]
"@components/*" = "./components/*"
"@utils/*" = "./utils/*"

[plugins.client.configs.tailwind]
# Generates tailwind.config.js
content = ["./src/**/*.{jac,tsx,jsx}"]

# Private/scoped npm registries
[plugins.client.npm.scoped_registries]
"@mycompany" = "https://npm.pkg.github.com"

[plugins.client.npm.auth."//npm.pkg.github.com/"]
_authToken = "${NODE_AUTH_TOKEN}"

# Global npm settings
[plugins.client.npm.settings]
always-auth = true

NPM Registry Configuration#

The [plugins.client.npm] section configures custom npm registries and authentication for private or scoped packages. This generates an .npmrc file automatically during dependency installation, eliminating the need to manage .npmrc files manually.
Key 	Type 	Description
settings 	dict 	Global .npmrc key-value settings (registry, always-auth, strict-ssl, proxy, etc.)
scoped_registries 	dict 	Maps npm scopes to registry URLs
auth 	dict 	Registry authentication tokens

Global settings emit arbitrary .npmrc key-value pairs:

[plugins.client.npm.settings]
registry = "https://registry.internal.example.com"
always-auth = true
strict-ssl = false
proxy = "http://proxy.company.com:8080"

Scoped registries map @scope prefixes to custom registry URLs:

[plugins.client.npm.scoped_registries]
"@mycompany" = "https://npm.pkg.github.com"
"@internal" = "https://registry.internal.example.com"

Auth tokens configure authentication for each registry. Use environment variables to avoid committing secrets:

[plugins.client.npm.auth."//npm.pkg.github.com/"]
_authToken = "${NODE_AUTH_TOKEN}"

The ${NODE_AUTH_TOKEN} syntax is resolved via the existing jac.toml environment variable interpolation. If the variable is not set at config load time, it passes through as a literal ${NODE_AUTH_TOKEN} in the generated .npmrc, which npm and bun also resolve natively.

The generated .npmrc is placed in .jac/client/configs/ and is automatically applied when Jac installs dependencies (e.g., via jac add --npm, jac start, or jac build).
Import Path Aliases#

The [plugins.client.paths] section lets you define custom import path aliases. Aliases are automatically applied to the generated Vite resolve.alias and TypeScript compilerOptions.paths, so both bundling and IDE autocompletion work out of the box.

[plugins.client.paths]
"@components/*" = "./components/*"
"@utils/*" = "./utils/*"
"@shared" = "./shared/index"

With the above config, you can use aliases in your .cl.jac or cl {} code:

cl {
    
import from "@components/Button" { Button }
    
import from "@utils/format" { formatDate }
    
import from "@shared" { constants }
}

Feature 	How It's Applied
Vite 	Added to resolve.alias in vite.config.js - resolves @components/Button to ./components/Button at build time
TypeScript 	Added to compilerOptions.paths in tsconfig.json with baseUrl: "." - enables IDE autocompletion and type checking
Module resolver 	The Jac compiler resolves aliases during compilation, so import from "@components/Button" finds the correct file

Wildcard patterns (@alias/* -> ./path/*) match any sub-path under the prefix. Exact patterns (@alias -> ./path) match only the alias itself.
CLI Commands#
Quick Reference#
Command 	Description
jac create myapp --use client 	Create new full-stack project
jac start 	Start dev server
jac start --dev 	Dev server with HMR
jac start --client pwa 	Start PWA (builds then serves)
jac start --client desktop 	Start desktop app in dev mode
jac build 	Build for production (web)
jac build --client desktop 	Build desktop app
jac build --client pwa 	Build PWA with offline support
jac setup desktop 	One-time desktop target setup (Tauri)
jac setup pwa 	One-time PWA setup (icons directory)
jac add --npm <pkg> 	Add npm package
jac add --npm --dev <pkg> 	Add npm dev dependency
jac add --npm 	Install all npm dependencies from jac.toml
jac remove --npm <pkg> 	Remove npm package

npm dependencies can also be declared in jac.toml:

[dependencies.npm]
lodash = "^4.17.21"
axios = "^1.6.0"

For private packages from custom registries, see NPM Registry Configuration above.
jac build#

Build a Jac application for a specific target.

jac
 build [filename] [--client TARGET] [-p PLATFORM]

Option 	Description 	Default
filename 	Path to .jac file 	main.jac
--client 	Build target (web, desktop, pwa) 	web
-p, --platform 	Desktop platform (windows, macos, linux, all) 	Current platform

Examples:

# Build web target (default)
jac
 build

# Build specific file
jac
 build main.jac

# Build PWA with offline support
jac
 build --client pwa

# Build desktop app for current platform
jac
 build --client desktop

# Build for a specific platform
jac
 build --client desktop --platform windows

# Build for all platforms
jac
 build --client desktop --platform all

jac setup#

One-time initialization for a build target.

jac
 setup <target>

Option 	Description
target 	Target to setup (desktop, pwa)

Examples:

# Setup desktop target (creates src-tauri/ directory)
jac
 setup desktop

# Setup PWA target (creates pwa_icons/ directory)
jac
 setup pwa

Extended Core Commands#

jac-client extends several core commands:
Command 	Added Option 	Description
jac create 	--use client 	Create full-stack project template
jac create 	--skip 	Skip npm package installation
jac start 	--client <target> 	Client build target for dev server
jac add 	--npm 	Add npm (client-side) dependency
jac add 	--npm --dev 	Add npm dev dependency
jac remove 	--npm 	Remove npm (client-side) dependency
Multi-Target Architecture#

jac-client supports building for multiple deployment targets from a single codebase.
Target 	Command 	Output 	Setup Required
Web (default) 	jac build 	.jac/client/dist/ 	No
Desktop (Tauri) 	jac build --client desktop 	Native installers 	Yes
PWA 	jac build --client pwa 	Installable web app 	No
Web Target (Default)#

Standard browser deployment using Vite:

jac
 build                    # Build for web
jac
 start --dev              # Dev server with HMR

Output: .jac/client/dist/ with index.html, bundled JS, and CSS.
Desktop Target (Tauri)#

Native desktop applications using Tauri. Creates installers for Windows, macOS, and Linux.

Prerequisites:

    Rust/Cargo: rustup.rs
    Build tools (platform-specific)

Setup & Build:

# 1. One-time setup (creates src-tauri/ directory)
jac
 setup desktop

# 2. Development with hot reload
jac
 start main.jac --client desktop --dev

# 3. Build installer for current platform
jac
 build --client desktop

# 4. Build for specific platform
jac
 build --client desktop --platform windows
jac
 build --client desktop --platform macos
jac
 build --client desktop --platform linux

Output: Installers in src-tauri/target/release/bundle/:

    Windows: .exe installer
    macOS: .dmg or .app bundle
    Linux: .AppImage, .deb, or .rpm

Configuration: Edit src-tauri/tauri.conf.json to customize window size, title, and app metadata.
PWA Target#

Progressive Web App with offline support, installability, and native-like experience.

Features:

    Offline support via Service Worker
    Installable on devices
    Auto-generated manifest.json
    Automatic icon generation (with Pillow)

Setup & Build:

# Optional: One-time setup (creates pwa_icons/ directory)
jac
 setup pwa

# Build PWA (includes manifest + service worker)
jac
 build --client pwa

# Development (service worker disabled for better DX)
jac
 start --client pwa --dev

# Production (builds PWA then serves)
jac
 start --client pwa

Output: Web bundle + manifest.json + sw.js (service worker)

Configuration in jac.toml:

[plugins.client.pwa]
theme_color = "#000000"
background_color = "#ffffff"
cache_name = "my-app-cache-v1"

[plugins.client.pwa.manifest]
name = "My App"
short_name = "App"
description = "My awesome Jac app"

Custom Icons: Add pwa-192x192.png and pwa-512x512.png to pwa_icons/ directory.
Automatic Endpoint Caching#

The client runtime automatically caches responses from reader endpoints and invalidates caches when writer endpoints are called. This uses compiler-provided endpoint_effects metadata -- no manual cache annotations or jacInvalidate() calls needed.

How it works:

    The compiler classifies each walker/function endpoint as a reader (no side effects) or writer (modifies state)
    Reader responses are stored in an LRU cache (500 entries, 60-second TTL)
    Concurrent identical requests are deduplicated (only one network call)
    When a writer endpoint is called, all cached reader responses are automatically invalidated
    Auth state changes (login/logout) clear the entire cache

This means spawning the same walker twice in quick succession only makes one API call, and creating/updating data automatically refreshes any cached reads.
BrowserRouter (Clean URLs)#

jac-client uses BrowserRouter for client-side routing, producing clean URLs like /about and /users/123 instead of hash-based URLs like #/about.

For this to work in production, your server must return the SPA HTML for all non-API routes. When using jac start, this is handled automatically -- the server's catch-all route serves the SPA HTML for extensionless paths, excluding API prefixes (cl/, walker/, function/, user/, static/).

The Vite dev server is configured with appType: 'spa' for history API fallback during development.
Build Error Diagnostics#

When client builds fail, jac-client displays structured error diagnostics instead of raw Vite/Rollup output. Errors include:

    Error codes (JAC_CLIENT_001, JAC_CLIENT_003, etc.)
    Source snippets pointing to the original .jac file location
    Actionable hints and quick fix commands

Code 	Issue 	Example Fix
JAC_CLIENT_001 	Missing npm dependency 	jac add --npm <package>
JAC_CLIENT_003 	Syntax error in client code 	Check source snippet
JAC_CLIENT_004 	Unresolved import 	Verify import path

To see raw error output alongside formatted diagnostics, set debug = true under [plugins.client] in jac.toml or set the JAC_DEBUG=1 environment variable.

    Note: Debug mode is enabled by default for a better development experience. For production deployments, set debug = false in jac.toml.

Build-Time Constants#

Define global variables that are replaced at compile time using the [plugins.client.vite.define] section in jac.toml:

[plugins.client.vite.define]
"globalThis.API_URL" = "\"https://api.example.com\""
"globalThis.FEATURE_ENABLED" = true
"globalThis.BUILD_VERSION" = "\"1.2.3\""

These values are inlined by Vite during bundling. String values must be double-quoted (JSON-encoded). Access them in client code:

cl {
    
def:pub Footer() -> JsxElement {
        
return <p>Version: {globalThis.BUILD_VERSION}</p>;
    
}
}

Development Server#
Prerequisites#

jac-client uses Bun for package management and JavaScript bundling. If Bun is not installed, the CLI prompts you to install it automatically.
Start Server#

# Basic
jac
 start main.jac

# With hot module replacement
jac
 start main.jac --dev

# HMR without client bundling (API only)
jac
 start main.jac --dev --no-client

# Dev server for desktop target
jac
 start main.jac --client desktop

API Proxy#

In dev mode, API routes are automatically proxied:

    /walker/* → Backend
    /function/* → Backend
    /user/* → Backend

Event Handlers#

cl {
    
def:pub Form() -> JsxElement {
        
has value: str = "";

        
return <div>
            <input
                value={value}
                onChange={lambda e: any -> None { value = e.target.value; }}
                onKeyPress={lambda e: any -> None {
                    
if e.key == "Enter" { submit(); }
                
}}
            
/>
            
<button onClick={lambda -> None { submit(); }}>
                Submit
            </button>
        
</div>;
    
}
}

Conditional Rendering#

cl {
    
def:pub ConditionalComponent() -> JsxElement {
        
has show: bool = False;
        
has items: list = [];

        
if show {
            
content = <p>Visible</p>;
        
} else {
            
content = <p>Hidden</p>;
        
}
        
return <div>
            {content}

            {show and <p>Only when true</p>}

            {[<li key={item["id"]}>{item["name"]}</li> for item in items]}
        
</div>;
    
}
}

Error Handling#
JacClientErrorBoundary#

JacClientErrorBoundary is a specialized error boundary component that catches rendering errors in your component tree, logs them, and displays a fallback UI, preventing the entire app from crashing when a descendant component fails.
Quick Start#

Import and wrap JacClientErrorBoundary around any subtree where you want to catch render-time errors:

cl import from "@jac/runtime" { JacClientErrorBoundary }

cl {
    
def:pub app() -> any {
        
return <JacClientErrorBoundary fallback={<div>Oops! Something went wrong.</div>}>
            <MainAppComponents />
        </JacClientErrorBoundary>;
    
}
}

Built-in Wrapping#

By default, jac-client internally wraps your entire application with JacClientErrorBoundary. This means:

    You don't need to manually wrap your root app component
    Errors in any component are caught and handled gracefully
    The app continues to run and displays a fallback UI instead of crashing

Props#
Prop 	Type 	Description
fallback 	JsxElement 	Custom fallback UI to show on error
FallbackComponent 	Component 	Show default fallback UI with error
children 	JsxElement 	Components to protect
Example with Custom Fallback#

cl {
    
def:pub App() -> any {
        
return <JacClientErrorBoundary fallback={<div className="error">Component failed to load</div>}>
            <ExpensiveWidget />
        </JacClientErrorBoundary>;
    
}
}

Nested Boundaries#

You can nest multiple error boundaries for fine-grained error isolation:

cl {
    
def:pub App() -> any {
        
return <JacClientErrorBoundary fallback={<div>App error</div>}>
            <Header />
            <JacClientErrorBoundary fallback={<div>Content error</div>}>
                <MainContent />
            </JacClientErrorBoundary>
            <Footer />
        </JacClientErrorBoundary>;
    
}
}

If MainContent throws an error, only that boundary's fallback is shown, while Header and Footer continue rendering normally.
Use Cases#

    Isolate Failure-Prone Widgets: Protect sections that fetch data, embed third-party code, or are unstable
    Per-Page Protection: Wrap top-level pages/routes to prevent one error from failing the whole app
    Micro-Frontend Boundaries: Nest boundaries around embeddables for fault isolation

Memory & Persistence#
Memory Hierarchy#
Tier 	Type 	Implementation
L1 	Volatile 	VolatileMemory (in-process)
L2 	Cache 	LocalCacheMemory (TTL-based)
L3 	Persistent 	SqliteMemory (default)
TieredMemory#

Automatic read-through caching and write-through persistence:

# Objects are automatically persisted
node User {
    
has name: str;
}

with entry {
    
user_node = User(name="Alice");
    
# Manual save
    
save(user_node);
    
commit();
}

ExecutionContext#

Manages runtime context:

    system_root -- System-level root node
    user_root -- User-specific root node
    entry_node -- Current entry point
    Memory -- Storage backend

Anchor Management#

Anchors provide persistent object references across sessions, allowing nodes and edges to be retrieved by stable identifiers after server restarts or session changes.
Development Tools#
Hot Module Replacement (HMR)#

# Enable with --dev flag
jac
 start main.jac --dev

Changes to .jac files automatically reload without restart.
Debug Mode#

jac
 debug main.jac

Provides:

    Step-through execution
    Variable inspection
    Breakpoints
    Graph visualization

Related Resources#

    Fullstack Setup Tutorial
    Components Tutorial
    State Management Tutorial
    Backend Integration Tutorial
    Authentication Tutorial
    Routing Tutorial

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
jac-scale Reference
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
            jac-scale Reference
            Learn by Doing
        Developer Workflow
        Python Integration
        Quick Reference

Table of contents

    Installation
    Starting a Server
        Basic Server
        Server Options
        Examples
        Default Persistence
        CORS Configuration
    API Endpoints
        Automatic Endpoint Generation
        Request Format
        Response Format
    Middleware Walkers
        Request Logging
        Authentication Middleware
    @restspec Decorator
        Options
        Custom HTTP Method
        Custom Path
        Path Parameters
        Functions
        Webhook Mode
    Authentication
        User Registration
        User Login
        Authenticated Requests
        JWT Configuration
        SSO (Single Sign-On)
    Admin Portal
        Accessing the Admin Portal
        Configuration
        User Roles
        Admin API Endpoints
    Permissions & Access Control
        Access Levels
        Granting Permissions
            To Everyone
            To a Specific Root
        Revoking Permissions
            From Everyone
            From a Specific Root
        Secure-by-Default Endpoints
        Walker Access Levels
        Permission Functions Reference
    Webhooks
        Configuration
        Creating Webhook Walkers
            Basic Webhook Walker
            Important Notes
        API Key Management
            Creating an API Key
            Listing API Keys
        Calling Webhook Endpoints
            Generating the Signature
        Webhook vs Regular Walkers
        Webhook API Reference
            Webhook Endpoints
            API Key Endpoints
            Required Headers for Webhook Requests
    WebSockets
        Overview
        Creating WebSocket Walkers
            Basic WebSocket Walker (Public)
            Authenticated WebSocket Walker
            Broadcasting WebSocket Walker
            Private Broadcasting Walker
        Important Notes
    Storage
        The store() Builtin
        Storage Interface
        Usage Example
        Configuration
        StorageFactory (Advanced)
    Graph Traversal API
        Traverse Endpoint
        Parameters
        Example
    Async Walkers
    Direct Database Access (kvstore)
    MongoDB Operations
        Querying Persisted Nodes (find_nodes)
    Redis Operations
    Database Configuration
        Environment Variables
        Memory Hierarchy
    Kubernetes Deployment
        Memory Resource Configuration
        Deployment Modes
        Generated Resources
        Service Discovery
        Auto-Provisioning
        Horizontal Pod Autoscaling
        Deployment Status
        Resource Tagging
        Remove Deployment
        Environment Variables
        Package Version Pinning
    Health Checks
        Health Endpoint
        Readiness Check
    Builtins
        Root Access
        Memory Commit
    CLI Commands
    API Documentation
    Graph Visualization
    Prometheus Metrics
        Configuration
        Exposed Metrics
        Usage
    Kubernetes Secrets
        Configuration
        How It Works
        Example
    Setting Up Kubernetes
        Docker Desktop (Easiest)
        Minikube
        MicroK8s (Linux)
    Troubleshooting
        Application Not Accessible
        Database Connection Issues
        Build Failures (--build mode)
        General Debugging
    Library Mode
    Related Resources

    Full Reference
    Deployment & Scaling

jac-scale Reference#

Complete reference for jac-scale, the cloud-native deployment and scaling plugin for Jac.
Installation#

pip
 install jac-scale
jac
 plugins enable scale

Starting a Server#
Basic Server#

jac
 start app.jac

Server Options#
Option 	Description 	Default
--port -p 	Server port 	8000
--main -m 	Treat as __main__ 	false
--faux -f 	Print generated API docs only (no server) 	false
--dev -d 	Enable HMR (Hot Module Replacement) mode 	false
--api_port -a 	Separate API port for HMR mode (0=same as port) 	0
--no_client -n 	Skip client bundling/serving (API only) 	false
--profile 	Configuration profile to load (e.g. prod, staging) 	-
--client 	Client build target for dev server (web, desktop, pwa) 	-
--scale 	Deploy to a target platform instead of running locally 	false
--build -b 	Build and push Docker image (with --scale) 	false
--experimental -e 	Use experimental mode (install from repo instead of PyPI) 	false
--target -t 	Deployment target (kubernetes, aws, gcp) 	kubernetes
--registry -r 	Image registry (dockerhub, ecr, gcr) 	dockerhub
Examples#

# Custom port
jac
 start app.jac --port 3000

# Development with HMR (requires jac-client)
jac
 start app.jac --dev

# API only -- skip client bundling
jac
 start app.jac --dev --no-client

# Preview generated API endpoints without starting
jac
 start app.jac --faux

# Production with profile
jac
 start app.jac --port 8000 --profile prod

Default Persistence#

When running locally (without --scale), Jac uses SQLite for graph persistence by default. You'll see "Using SQLite for persistence" in the server output. No external database setup is required for development.
CORS Configuration#

[plugins.scale.cors]
allow_origins = ["https://example.com"]
allow_methods = ["GET", "POST", "PUT", "DELETE"]
allow_headers = ["*"]

API Endpoints#
Automatic Endpoint Generation#

Each walker becomes an API endpoint:

walker get_users {
    
can fetch with Root entry {
        
report [];
    
}
}

Becomes: POST /walker/get_users
Request Format#

Walker parameters become request body:

walker search {
    
has query: str;
    
has limit: int = 10;
}

curl
 -X POST http://localhost:8000/walker/search \
  -H "Content-Type: application/json" \
  -d '{"query": "hello", "limit": 20}'

Response Format#

Walker report values become the response.
Middleware Walkers#

Walkers prefixed with _ act as middleware hooks that run before or around normal request processing.
Request Logging#

walker _before_request {
    
has request: dict;

    
can log with Root entry {
        
print(f"Request: {self.request['method']} {self.request['path']}");
    
}
}

Authentication Middleware#

walker _authenticate {
    
has headers: dict;

    
can check with Root entry {
        
token = self.headers.get("Authorization", "");

        
if not token.startswith("Bearer ") {
            
report {"error": "Unauthorized", "status": 401};
            
return;
        
}

        
# Validate token...
        
report {"authenticated": True};
    
}
}

Middleware vs Built-in Auth

The _authenticate middleware pattern gives you custom authentication logic. For standard JWT authentication, use jac-scale's built-in auth endpoints (/user/register, /user/login) instead -- see Authentication below.
@restspec Decorator#

The @restspec decorator customizes how walkers and functions are exposed as REST API endpoints.
Options#
Option 	Type 	Default 	Description
method 	HTTPMethod 	POST 	HTTP method for the endpoint
path 	str 	"" (auto-generated) 	Custom URL path for the endpoint
protocol 	APIProtocol 	APIProtocol.HTTP 	Protocol for the endpoint (HTTP, WEBHOOK, or WEBSOCKET)
broadcast 	bool 	False 	Broadcast responses to all connected WebSocket clients (only valid with WEBSOCKET protocol)

    Note: APIProtocol and restspec are builtins and do not require an import statement. HTTPMethod must be imported with import from http { HTTPMethod }.

Custom HTTP Method#

By default, walkers are exposed as POST endpoints. Use @restspec to change this:

import from http { HTTPMethod }

@restspec(method=HTTPMethod.GET)
walker :pub get_users {
    
can fetch with Root entry {
        
report [];
    
}
}

This walker is now accessible at GET /walker/get_users instead of POST.
Custom Path#

Override the auto-generated path:

@restspec(method=HTTPMethod.GET, path="/custom/users")
walker :pub list_users {
    
can fetch with Root entry {
        
report [];
    
}
}

Accessible at GET /custom/users.
Path Parameters#

Define path parameters using {param_name} syntax:

import from http { HTTPMethod }

@restspec(method=HTTPMethod.GET, path="/items/{item_id}")
walker :pub get_item {
    
has item_id: str;
    
can fetch with Root entry { report {"item_id": self.item_id}; }
}

@restspec(method=HTTPMethod.GET, path="/users/{user_id}/orders")
walker :pub get_user_orders {
    
has user_id: str;          # Path parameter
    
has status: str = "all";   # Query parameter
    
can fetch with Root entry { report {"user_id": self.user_id, "status": self.status}; }
}

Parameters are classified as: path (matches {name} in path) → file (UploadFile type) → query (GET) → body (other methods).
Functions#

@restspec also works on standalone functions:

@restspec(method=HTTPMethod.GET)
def :pub health_check() -> dict {
    
return {"status": "healthy"};
}

@restspec(method=HTTPMethod.GET, path="/custom/status")
def :pub app_status() -> dict {
    
return {"status": "running", "version": "1.0.0"};
}

Webhook Mode#

See the Webhooks section below.
Authentication#
User Registration#

curl
 -X POST http://localhost:8000/user/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'

User Login#

curl
 -X POST http://localhost:8000/user/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'

Returns:

{
  "access_token": "eyJ...",
  "token_type": "bearer"
}

Authenticated Requests#

curl
 -X POST http://localhost:8000/walker/my_walker \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{}'

JWT Configuration#

Configure JWT authentication via environment variables:
Variable 	Description 	Default
JWT_SECRET 	Secret key for JWT signing 	supersecretkey
JWT_ALGORITHM 	JWT algorithm 	HS256
JWT_EXP_DELTA_DAYS 	Token expiration in days 	7
SSO (Single Sign-On)#

jac-scale supports SSO with external identity providers. Currently supported: Google.

Configuration:
Variable 	Description
SSO_HOST 	SSO callback host URL (default: http://localhost:8000/sso)
SSO_GOOGLE_CLIENT_ID 	Google OAuth client ID
SSO_GOOGLE_CLIENT_SECRET 	Google OAuth client secret

SSO Endpoints:
Method 	Path 	Description
GET 	/sso/{platform}/login 	Redirect to provider login page
GET 	/sso/{platform}/register 	Redirect to provider registration
GET 	/sso/{platform}/login/callback 	OAuth callback handler

Frontend Callback Redirect:

For browser-based OAuth flows, configure client_auth_callback_url in jac.toml to redirect the SSO callback to your frontend application instead of returning JSON:

[plugins.scale.sso]
client_auth_callback_url = "http://localhost:3000/auth/callback"

When set, the callback endpoint redirects to the configured URL with query parameters:

    On success: {client_auth_callback_url}?token={jwt_token}
    On failure: {client_auth_callback_url}?error={error_message}

This enables seamless browser-based OAuth flows where the frontend receives the token via URL parameters.

Example:

# Redirect user to Google login
curl
 http://localhost:8000/sso/google/login

Admin Portal#

jac-scale includes a built-in admin portal for managing users, roles, and SSO configurations.
Accessing the Admin Portal#

Navigate to http://localhost:8000/admin to access the admin dashboard. On first server start, an admin user is automatically bootstrapped.
Configuration#

[plugins.scale.admin]
enabled = true
username = "admin"
session_expiry_hours = 24

Option 	Type 	Default 	Description
enabled 	bool 	true 	Enable/disable admin portal
username 	string 	"admin" 	Admin username
session_expiry_hours 	int 	24 	Admin session duration in hours

Environment Variables:
Variable 	Description
ADMIN_USERNAME 	Admin username (overrides jac.toml)
ADMIN_EMAIL 	Admin email (overrides jac.toml)
ADMIN_DEFAULT_PASSWORD 	Initial password (overrides jac.toml)
User Roles#
Role 	Value 	Description
ADMIN 	admin 	Full administrative access
MODERATOR 	moderator 	Limited administrative access
USER 	user 	Standard user access
Admin API Endpoints#
Method 	Path 	Description
POST 	/admin/login 	Admin authentication
GET 	/admin/users 	List all users
GET 	/admin/users/{username} 	Get user details
POST 	/admin/users 	Create a new user
PUT 	/admin/users/{username} 	Update user role/settings
DELETE 	/admin/users/{username} 	Delete a user
POST 	/admin/users/{username}/force-password-reset 	Force password reset
GET 	/admin/sso/providers 	List SSO providers
GET 	/admin/sso/users/{username}/accounts 	Get user's SSO accounts
Permissions & Access Control#
Access Levels#
Level 	Value 	Description
NO_ACCESS 	-1 	No access to the object
READ 	0 	Read-only access
CONNECT 	1 	Can traverse edges to/from this object
WRITE 	2 	Full read/write access
Granting Permissions#
To Everyone#

Use perm_grant to allow all users to access an object at a given level:

with entry {
    
# Allow everyone to read this node
    
perm_grant(node, READ);

    
# Allow everyone to write
    
perm_grant(node, WRITE);
}

To a Specific Root#

Use allow_root to grant access to a specific user's root graph:

with entry {
    
# Allow a specific user to read this node
    
allow_root(node, target_root_id, READ);

    
# Allow write access
    
allow_root(node, target_root_id, WRITE);
}

Revoking Permissions#
From Everyone#

with entry {
    
# Revoke all public access
    
perm_revoke(node);
}

From a Specific Root#

with entry {
    
# Revoke a specific user's access
    
disallow_root(node, target_root_id, READ);
}

Secure-by-Default Endpoints#

All walker and function endpoints are protected by default -- they require JWT authentication. You must explicitly opt-in to public access using the :pub modifier. This secure-by-default approach prevents accidentally exposing endpoints without authentication.

# Protected (default) -- requires JWT token
walker get_profile {
    
can fetch with Root entry { report [-->]; }
}

# Public -- no authentication required
walker :pub health_check {
    
can check with Root entry { report {"status": "ok"}; }
}

# Private -- requires authentication, per-user isolated
walker :priv internal_process {
    
can run with Root entry { }
}

Walker Access Levels#

Walkers have three access levels when served as API endpoints:
Access 	Description
Public (:pub) 	Accessible without authentication
Protected (default) 	Requires JWT authentication
Private (:priv) 	Requires JWT authentication; per-user isolated (each user operates on their own graph)
Permission Functions Reference#
Function 	Signature 	Description
perm_grant 	perm_grant(archetype, level) 	Allow everyone to access at given level
perm_revoke 	perm_revoke(archetype) 	Remove all public access
allow_root 	allow_root(archetype, root_id, level) 	Grant access to a specific root
disallow_root 	disallow_root(archetype, root_id, level) 	Revoke access from a specific root
Webhooks#

Webhooks allow external services (payment processors, CI/CD systems, messaging platforms, etc.) to send real-time notifications to your Jac application. Jac-Scale provides:

    Dedicated /webhook/ endpoints for webhook walkers
    API key authentication for secure access
    HMAC-SHA256 signature verification to validate request integrity
    Automatic endpoint generation based on walker configuration

Configuration#

Webhook configuration is managed via the jac.toml file in your project root.

[plugins.scale.webhook]
secret = "your-webhook-secret-key"
signature_header = "X-Webhook-Signature"
verify_signature = true
api_key_expiry_days = 365

Option 	Type 	Default 	Description
secret 	string 	"webhook-secret-key" 	Secret key for HMAC signature verification. Can also be set via WEBHOOK_SECRET environment variable.
signature_header 	string 	"X-Webhook-Signature" 	HTTP header name containing the HMAC signature.
verify_signature 	boolean 	true 	Whether to verify HMAC signatures on incoming requests.
api_key_expiry_days 	integer 	365 	Default expiry period for API keys in days. Set to 0 for permanent keys.

Environment Variables:

For production deployments, use environment variables for sensitive values:

export WEBHOOK_SECRET="your-secure-random-secret"

Creating Webhook Walkers#

To create a webhook endpoint, use the @restspec(protocol=APIProtocol.WEBHOOK) decorator on your walker definition.
Basic Webhook Walker#

@restspec(protocol=APIProtocol.WEBHOOK)
walker PaymentReceived {
    
has payment_id: str,
        
amount: float,
        
currency: str = 'USD';

    
can process with Root entry {
        
# Process the payment notification
        
report {
            
"status": "success",
            
"message": f"Payment {self.payment_id} received",
            
"amount": self.amount,
            
"currency": self.currency
        
};
    
}
}

This walker will be accessible at POST /webhook/PaymentReceived.
Important Notes#

    Webhook walkers are only accessible via /webhook/{walker_name} endpoints
    They are not accessible via the standard /walker/{walker_name} endpoint

API Key Management#

Webhook endpoints require API key authentication. Users must first create an API key before calling webhook endpoints.

    Note: API key metadata is stored persistently in MongoDB (in the webhook_api_keys collection), so keys survive server restarts. Previously, keys were held in memory only.

Creating an API Key#

Endpoint: POST /api-key/create

Headers:

    Authorization: Bearer <jwt_token> (required)

Request Body:

{
    "name": "My Webhook Key",
    "expiry_days": 30
}

Response:

{
    "api_key": "eyJhbGciOiJIUzI1NiIs...",
    "api_key_id": "a1b2c3d4e5f6...",
    "name": "My Webhook Key",
    "created_at": "2024-01-15T10:30:00Z",
    "expires_at": "2024-02-14T10:30:00Z"
}

Listing API Keys#

Endpoint: GET /api-key/list

Headers:

    Authorization: Bearer <jwt_token> (required)

Calling Webhook Endpoints#

Webhook endpoints require two headers for authentication:

    X-API-Key: The API key obtained from /api-key/create
    X-Webhook-Signature: HMAC-SHA256 signature of the request body

Generating the Signature#

The signature is computed as: HMAC-SHA256(request_body, api_key)

cURL Example:

API_KEY="eyJhbGciOiJIUzI1NiIs..."
PAYLOAD='{"payment_id":"PAY-12345","amount":99.99,"currency":"USD"}'
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$API_KEY" | cut -d' ' -f2)

curl
 -X POST "http://localhost:8000/webhook/PaymentReceived" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $API_KEY" \
    -H "X-Webhook-Signature: $SIGNATURE" \
    -d "$PAYLOAD"

Webhook vs Regular Walkers#
Feature 	Regular Walker (/walker/) 	Webhook Walker (/webhook/)
Authentication 	JWT Bearer token 	API Key + HMAC Signature
Use Case 	User-facing APIs 	External service callbacks
Access Control 	User-scoped 	Service-scoped
Signature Verification 	No 	Yes (HMAC-SHA256)
Endpoint Path 	/walker/{name} 	/webhook/{name}
Webhook API Reference#
Webhook Endpoints#
Method 	Path 	Description
POST 	/webhook/{walker_name} 	Execute webhook walker
API Key Endpoints#
Method 	Path 	Description
POST 	/api-key/create 	Create a new API key
GET 	/api-key/list 	List all API keys for user
DELETE 	/api-key/{api_key_id} 	Revoke an API key
Required Headers for Webhook Requests#
Header 	Required 	Description
Content-Type 	Yes 	Must be application/json
X-API-Key 	Yes 	API key from /api-key/create
X-Webhook-Signature 	Yes* 	HMAC-SHA256 signature (*if verify_signature is enabled)
WebSockets#

Jac Scale provides built-in support for WebSocket endpoints, enabling real-time bidirectional communication between clients and walkers.
Overview#

WebSockets allow persistent, full-duplex connections between a client and your Jac application. Unlike REST endpoints (single request-response), a WebSocket connection stays open, allowing multiple messages to be exchanged in both directions. Jac Scale provides:

    Dedicated /ws/ endpoints for WebSocket walkers
    Persistent connections with a message loop
    JSON message protocol for sending walker fields and receiving results
    JWT authentication via query parameter or message payload
    Connection management with automatic cleanup on disconnect
    HMR support in dev mode for live reloading

Creating WebSocket Walkers#

To create a WebSocket endpoint, use the @restspec(protocol=APIProtocol.WEBSOCKET) decorator on an async walker definition.
Basic WebSocket Walker (Public)#

@restspec(protocol=APIProtocol.WEBSOCKET)
async walker : pub EchoMessage {
    
has message: str;
    
has client_id: str = "anonymous";

    
async can echo with Root entry {
        
report {
            
"echo": self.message,
            
"client_id": self.client_id
        
};
    
}
}

This walker will be accessible at ws://localhost:8000/ws/EchoMessage.
Authenticated WebSocket Walker#

To create a private walker that requires JWT authentication, simply remove : pub from the walker definition.
Broadcasting WebSocket Walker#

Use broadcast=True to send messages to ALL connected clients of this walker:

@restspec(protocol=APIProtocol.WEBSOCKET, broadcast=True)
async walker : pub ChatRoom {
    
has message: str;
    
has sender: str = "anonymous";

    
async can handle with Root entry {
        
report {
            
"type": "message",
            
"sender": self.sender,
            
"content": self.message
        
};
    
}
}

When a client sends a message, all connected clients receive the response, making it ideal for:

    Chat rooms
    Live notifications
    Real-time collaboration
    Game state synchronization

Private Broadcasting Walker#

To create a private broadcasting walker, remove : pub from the walker definition. Only authenticated users can connect and send messages, and all authenticated users receive broadcasts.
Important Notes#

    WebSocket walkers must be declared as async walker
    Use : pub for public access (no authentication required) or omit it to require JWT auth
    Use broadcast=True to send responses to ALL connected clients (only valid with WEBSOCKET protocol)
    WebSocket walkers are only accessible via ws://host/ws/{walker_name}
    The connection stays open until the client disconnects

Storage#

Jac provides a built-in storage abstraction for file and blob operations. The core runtime ships with a local filesystem implementation, and jac-scale can override it with cloud storage backends -- all through the same store() builtin.
The store() Builtin#

The recommended way to get a storage instance is the store() builtin. It requires no imports and is automatically hookable by plugins:

# Get a storage instance (no imports needed)
glob storage = store();

# With custom base path
glob storage = store(base_path="./uploads");

# With all options
glob storage = store(base_path="./uploads", create_dirs=True);

Parameter 	Type 	Default 	Description
base_path 	str 	"./storage" 	Root directory for all files
create_dirs 	bool 	True 	Create base directory if it doesn't exist

Without jac-scale, store() returns a LocalStorage instance. With jac-scale installed, it returns a configuration-driven backend (reading from jac.toml and environment variables).
Storage Interface#

All storage instances provide these methods:
Method 	Signature 	Description
upload 	upload(source, destination, metadata=None) -> str 	Upload a file (from path or file object)
download 	download(source, destination=None) -> bytes\|None 	Download a file (returns bytes if no destination)
delete 	delete(path) -> bool 	Delete a file or directory
exists 	exists(path) -> bool 	Check if a path exists
list_files 	list_files(prefix="", recursive=False) 	List files (yields paths)
get_metadata 	get_metadata(path) -> dict 	Get file metadata (size, modified, created, is_dir, name)
copy 	copy(source, destination) -> bool 	Copy a file within storage
move 	move(source, destination) -> bool 	Move a file within storage
Usage Example#

import from http { UploadFile }
import from uuid { uuid4 }

glob storage = store(base_path="./uploads");

walker :pub upload_file {
    
has file: UploadFile;
    
has folder: str = "documents";

    
can process with Root entry {
        
unique_name = f"{uuid4()}.dat";
        
path = f"{self.folder}/{unique_name}";

        
# Upload file
        
storage.upload(self.file.file, path);

        
# Get metadata
        
metadata = storage.get_metadata(path);

        
report {
            
"success": True,
            
"storage_path": path,
            
"size": metadata["size"]
        
};
    
}
}

walker :pub list_files {
    
has folder: str = "documents";
    
has recursive: bool = False;

    
can process with Root entry {
        
files = [];
        
for path in storage.list_files(self.folder, self.recursive) {
            
metadata = storage.get_metadata(path);
            
files.append({
                
"path": path,
                
"size": metadata["size"],
                
"name": metadata["name"]
            
});
        
}
        
report {"files": files};
    
}
}

walker :pub download_file {
    
has path: str;

    
can process with Root entry {
        
if not storage.exists(self.path) {
            
report {"error": "File not found"};
            
return;
        
}
        
content = storage.download(self.path);
        
report {"content": content, "size": len(content)};
    
}
}

Configuration#

Configure storage in jac.toml:

[storage]
storage_type = "local"       # Storage backend type
base_path = "./storage"      # Base directory for files
create_dirs = true           # Auto-create directories

Option 	Type 	Default 	Description
storage_type 	string 	"local" 	Storage backend (local)
base_path 	string 	"./storage" 	Base path for file storage
create_dirs 	boolean 	true 	Automatically create directories

Environment Variables:
Variable 	Description
JAC_STORAGE_TYPE 	Storage type (overrides jac.toml)
JAC_STORAGE_PATH 	Base directory (overrides jac.toml)
JAC_STORAGE_CREATE_DIRS 	Auto-create directories ("true"/"false")

Configuration priority: jac.toml > environment variables > defaults.
StorageFactory (Advanced)#

For advanced use cases, you can use StorageFactory directly instead of the store() builtin:

import from jac_scale.factories.storage_factory { StorageFactory }

# Create with explicit type and config
glob config = {"base_path": "./my-files", "create_dirs": True};
glob storage = StorageFactory.create("local", config);

# Create using jac.toml / env var / defaults
glob default_storage = StorageFactory.get_default();

Graph Traversal API#
Traverse Endpoint#

POST
 /traverse

Parameters#
Parameter 	Type 	Description 	Default
source 	str 	Starting node/edge ID 	root
depth 	int 	Traversal depth 	1
detailed 	bool 	Include archetype context 	false
node_types 	list 	Filter by node types 	all
edge_types 	list 	Filter by edge types 	all
Example#

curl
 -X POST http://localhost:8000/traverse \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "depth": 3,
    "node_types": ["User", "Post"],
    "detailed": true
  }'

Async Walkers#

walker async_processor {
    
has items: list;

    
async can process with Root entry {
        
results = [];
        
for item in self.items {
            
result = await process_item(item);
            
results.append(result);
        
}
        
report results;
    
}
}

Direct Database Access (kvstore)#

Direct database operations without graph layer abstraction. Supports MongoDB (document queries) and Redis (key-value with TTL/atomic ops).

import from jac_scale.lib { kvstore }

with entry {
    
mongo_db = kvstore(db_name='my_app', db_type='mongodb');
    
redis_db = kvstore(db_name='cache', db_type='redis');
}

Parameters: db_name (str), db_type ('mongodb'|'redis'), uri (str|None - priority: explicit → MONGODB_URI/REDIS_URL env vars → jac.toml)
MongoDB Operations#

Common Methods: get(), set(), delete(), exists() Query Methods: find_one(), find(), insert_one(), insert_many(), update_one(), update_many(), delete_one(), delete_many(), find_by_id(), update_by_id(), delete_by_id(), find_nodes()

Example:

import from jac_scale.lib { kvstore }

with entry {
    
db = kvstore(db_name='my_app', db_type='mongodb');

    
db.insert_one('users', {'name': 'Alice', 'role': 'admin', 'age': 30});
    
alice = db.find_one('users', {'name': 'Alice'});
    
admins = list(db.find('users', {'role': 'admin'}));
    
older = list(db.find('users', {'age': {'$gt': 28}}));

    
db.update_one('users', {'name': 'Alice'}, {'$set': {'age': 31}});
    
db.delete_one('users', {'name': 'Bob'});

    
db.set('user:123', {'status': 'active'}, 'sessions');
}

Query Operators: $eq, $gt, $gte, $lt, $lte, $in, $ne, $and, $or
Querying Persisted Nodes (find_nodes)#

Query persisted graph nodes by type with MongoDB filters. Returns deserialized node instances.

with entry{
    
db = kvstore(db_name='jac_db', db_type='mongodb');
    
young_users = list(db.find_nodes('User', {'age': {'$lt': 30}}));
    
admins = list(db.find_nodes('User', {'role': 'admin'}));
}

Parameters: node_type (str), filter (dict, default {}), col_name (str, default '_anchors')
Redis Operations#

Common Methods: get(), set(), delete(), exists() Redis Methods: set_with_ttl(), expire(), incr(), scan_keys()

Example:

import from jac_scale.lib { kvstore }

with entry {
    
cache = kvstore(db_name='cache', db_type='redis');

    
cache.set('session:user123', {'user_id': '123', 'username': 'alice'});
    
cache.set_with_ttl('temp:token', {'token': 'xyz'}, ttl=60);
    
cache.set_with_ttl('cache:profile', {'name': 'Alice'}, ttl=3600);

    
cache.incr('stats:views');
    
sessions = cache.scan_keys('session:*');
    
cache.expire('session:user123', 1800);
}

Note: Database-specific methods raise NotImplementedError on wrong database type.
Database Configuration#
Environment Variables#
Variable 	Description 	Default
MONGODB_URI 	MongoDB connection URI 	None
REDIS_URL 	Redis connection URL 	None
K8s_MONGODB 	Enable MongoDB deployment 	false
K8s_REDIS 	Enable Redis deployment 	false
Memory Hierarchy#

jac-scale uses a tiered memory system:
Tier 	Backend 	Purpose
L1 	In-memory 	Volatile runtime state
L2 	Redis 	Cache layer
L3 	MongoDB 	Persistent storage

Application

L1: Volatile (in-memory)

L2: Redis (cache)

L3: MongoDB (persistent)
Kubernetes Deployment#
Memory Resource Configuration#

Control how much memory Kubernetes allows for your application container.
Parameter 	TOML Key 	Default 	Description
K8s_MEMORY_LIMIT 	memory_limit 	12Gi 	Maximum memory the container may use before being OOM-killed

Override the default in your jac.toml:

[plugins.scale.kubernetes]
memory_limit = "2Gi"

Accepted suffixes: Ki, Mi, Gi (binary) or K, M, G (decimal).
Deployment Modes#
Mode 	Command 	Use Case
Development 	jac start app.jac --scale 	Fast iteration -- deploys without building a Docker image
Production 	jac start app.jac --scale --build 	Builds and pushes Docker image to registry before deploying

Production mode requires Docker credentials:

# .env
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password-or-token

Generated Resources#

# Example generated deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jac-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: jac-app

Service Discovery#

Kubernetes service mesh integration for:

    Automatic load balancing
    Service-to-service communication
    Health monitoring

Auto-Provisioning#

On first deployment, jac start --scale automatically provisions:

    Redis -- StatefulSet with persistent storage (caching layer)
    MongoDB -- StatefulSet with persistent storage (graph persistence)
    Application Deployment -- Your Jac application pod(s)
    Services -- NodePort service for external access
    ConfigMaps -- Application configuration

Subsequent deployments only update the application -- databases persist across deployments.
Horizontal Pod Autoscaling#

jac-scale supports automatic horizontal scaling based on average CPU usage. When deployed to Kubernetes, pods are automatically scaled up or down based on load.

Autoscaling is configured through Kubernetes resource settings. Set CPU requests and limits via environment variables:

export K8s_CPU_REQUEST="250m"
export K8s_CPU_LIMIT="1000m"
export K8s_MEMORY_REQUEST="256Mi"
export K8s_MEMORY_LIMIT="512Mi"

Deployment Status#

Check the live status of all components in your Kubernetes deployment:

jac
 status app.jac

This queries the cluster and displays a table showing:

    Component health -- status of the Jaseci App, Redis, MongoDB, Prometheus, and Grafana
    Pod readiness -- ready vs total replica counts for each component
    Service URLs -- application and Grafana endpoints

Status values include Running, Degraded (partial readiness), Pending (starting up), Restarting (crash-looping pods), Failed, and Not Deployed.

The command makes efficient bulk API calls (listing all Deployments, StatefulSets, and Pods in the namespace at once) rather than querying each component individually.
Resource Tagging#

All Kubernetes resources created by jac-scale are automatically labeled with managed: jac-scale. This enables easy identification and auditing of jac-scale-owned resources:

# List all jac-scale managed resources across namespaces
kubectl
 get all -l managed=jac-scale -A

Tagged resources include Deployments, StatefulSets, Services, ConfigMaps, Secrets, PersistentVolumeClaims, and HorizontalPodAutoscalers.
Remove Deployment#

jac
 destroy app.jac

This removes all Kubernetes resources created by jac-scale:

    Application deployments and pods
    Redis and MongoDB StatefulSets
    Services and persistent volumes
    ConfigMaps and secrets

Environment Variables#
Variable 	Description 	Default
APP_NAME 	Application name for K8s resources 	jaseci
K8s_NAMESPACE 	Kubernetes namespace 	default
K8s_NODE_PORT 	External NodePort 	30001
K8s_CPU_REQUEST 	CPU resource request 	None
K8s_CPU_LIMIT 	CPU resource limit 	None
K8s_MEMORY_REQUEST 	Memory resource request 	None
K8s_MEMORY_LIMIT 	Memory resource limit 	None
K8s_READINESS_INITIAL_DELAY 	Readiness probe initial delay (seconds) 	10
K8s_READINESS_PERIOD 	Readiness probe period (seconds) 	20
K8s_LIVENESS_INITIAL_DELAY 	Liveness probe initial delay (seconds) 	10
K8s_LIVENESS_PERIOD 	Liveness probe period (seconds) 	20
K8s_REPLICAS 	Number of replicas 	1
K8s_LIVENESS_FAILURE_THRESHOLD 	Failure threshold before restart 	80
DOCKER_USERNAME 	DockerHub username 	None
DOCKER_PASSWORD 	DockerHub password/token 	None
Package Version Pinning#

Configure specific package versions for Kubernetes deployments:

[plugins.scale.kubernetes.plugin_versions]
jaclang = "0.1.5"      # Specific version
jac_scale = "latest"   # Latest from PyPI (default)
jac_client = "0.1.0"   # Specific version
jac_byllm = "none"     # Skip installation

Package 	Description 	Default
jaclang 	Core Jac language package 	latest
jac_scale 	Scaling plugin 	latest
jac_client 	Client/frontend support 	latest
jac_byllm 	LLM integration (use "none" to skip) 	latest
Health Checks#

Built-in endpoints are available for Kubernetes probes:

    /health -- Liveness probe
    /ready -- Readiness probe

You can also create custom health walkers:
Health Endpoint#

Create a health walker:

walker health {
    
can check with Root entry {
        
report {"status": "healthy"};
    
}
}

Access at: POST /walker/health
Readiness Check#

walker ready {
    
can check with Root entry {
        
db_ok = check_database();
        
cache_ok = check_cache();

        
if db_ok and cache_ok {
            
report {"status": "ready"};
        
} else {
            
report {
                
"status": "not_ready",
                
"db": db_ok,
                
"cache": cache_ok
            
};
        
}
    
}
}

Builtins#
Root Access#

with entry {
    
# Get all roots in memory/database
    
roots = allroots();
}

Memory Commit#

with entry {
    
# Commit memory to database
    
commit();
}

CLI Commands#
Command 	Description
jac start app.jac 	Start local API server
jac start app.jac --scale 	Deploy to Kubernetes
jac start app.jac --scale --build 	Build image and deploy
jac destroy app.jac 	Remove Kubernetes deployment
API Documentation#

When server is running:

    Swagger UI: http://localhost:8000/docs
    ReDoc: http://localhost:8000/redoc
    OpenAPI JSON: http://localhost:8000/openapi.json

Graph Visualization#

Navigate to http://localhost:8000/graph to view an interactive visualization of your application's graph directly in the browser.

    Without authentication - displays the public graph (super root), useful for applications with public endpoints
    With authentication - click the Login button in the header to sign in and view your user-specific graph

The visualizer uses a force-directed layout with color-coded node types, edge labels, tooltips on hover, and controls for refresh, fit-to-view, and physics toggle. If a user has previously logged in (via a jac-client app or the login modal), the existing jac_token in localStorage is picked up automatically.
Endpoint 	Description
GET /graph 	Serves the graph visualization UI
GET /graph/data 	Returns graph nodes and edges as JSON (optional Authorization header)
Prometheus Metrics#

jac-scale provides built-in Prometheus metrics collection for monitoring HTTP requests and walker execution. When enabled, a /metrics endpoint is automatically registered for Prometheus to scrape.
Configuration#

Configure metrics in jac.toml:

[plugins.scale.metrics]
enabled = true                  # Enable metrics collection and /metrics endpoint
endpoint = "/metrics"           # Prometheus scrape endpoint path
namespace = "myapp"             # Metrics namespace prefix
walker_metrics = true           # Enable per-walker execution timing
histogram_buckets = [0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 10.0]

Option 	Type 	Default 	Description
enabled 	bool 	false 	Enable Prometheus metrics collection and /metrics endpoint
endpoint 	string 	"/metrics" 	Path for the Prometheus scrape endpoint
namespace 	string 	"jac_scale" 	Metrics namespace prefix
walker_metrics 	bool 	false 	Enable walker execution timing metrics
histogram_buckets 	list 	[0.005, ..., 10.0] 	Histogram bucket boundaries in seconds

    Note: If namespace is not set, it is derived from the Kubernetes namespace config (sanitized) or defaults to "jac_scale".

Exposed Metrics#
Metric 	Type 	Labels 	Description
{namespace}_http_requests_total 	Counter 	method, path, status_code 	Total HTTP requests processed
{namespace}_http_request_duration_seconds 	Histogram 	method, path 	HTTP request latency in seconds
{namespace}_http_requests_in_progress 	Gauge 	-- 	Concurrent HTTP requests
{namespace}_walker_duration_seconds 	Histogram 	walker_name, success 	Walker execution duration (only when walker_metrics=true)
Usage#

# Scrape metrics
curl
 http://localhost:8000/metrics

The metrics endpoint is auto-registered as a GET route with OpenAPI tag "Monitoring". Requests to the metrics endpoint itself are excluded from tracking.
Kubernetes Secrets#

Manage sensitive environment variables securely in Kubernetes deployments using the [plugins.scale.secrets] section.
Configuration#

[plugins.scale.secrets]
OPENAI_API_KEY = "${OPENAI_API_KEY}"
DATABASE_PASSWORD = "${DB_PASS}"
STATIC_VALUE = "hardcoded-value"

Values using ${ENV_VAR} syntax are resolved from the local environment at deploy time. The resolved key-value pairs are created as a proper Kubernetes Secret ({app_name}-secrets) and injected into pods via envFrom.secretRef.
How It Works#

    At jac start --scale, environment variable references (${...}) are resolved
    A Kubernetes Opaque Secret named {app_name}-secrets is created (or updated if it already exists)
    The Secret is attached to the deployment pod spec via envFrom.secretRef
    All keys become environment variables inside the container
    On jac destroy, the Secret is automatically cleaned up

Example#

# jac.toml
[plugins.scale.secrets]
OPENAI_API_KEY = "${OPENAI_API_KEY}"
MONGO_PASSWORD = "${MONGO_PASSWORD}"
JWT_SECRET = "${JWT_SECRET}"

# Set local env vars, then deploy
export OPENAI_API_KEY="sk-..."
export MONGO_PASSWORD="secret123"
export JWT_SECRET="my-jwt-key"

jac
 start app.jac --scale --build

This eliminates the need for manual kubectl create secret commands after deployment.
Setting Up Kubernetes#
Docker Desktop (Easiest)#

    Install Docker Desktop
    Open Settings > Kubernetes
    Check "Enable Kubernetes"
    Click "Apply & Restart"

Minikube#

# Install
brew
 install minikube  # macOS
# or see https://minikube.sigs.k8s.io/docs/start/

# Start cluster
minikube
 start

# Access your app via minikube service
minikube
 service jaseci -n default

MicroK8s (Linux)#

sudo
 snap install microk8s --classic
microk8s
 enable dns storage
alias kubectl='microk8s kubectl'

Troubleshooting#
Application Not Accessible#

# Check pod status
kubectl
 get pods

# Check service
kubectl
 get svc

# For minikube, use tunnel
minikube
 service jaseci

Database Connection Issues#

# Check StatefulSets
kubectl
 get statefulsets

# Check persistent volumes
kubectl
 get pvc

# View database logs
kubectl
 logs -l app=mongodb
kubectl
 logs -l app=redis

Build Failures (--build mode)#

    Ensure Docker daemon is running
    Verify .env has correct DOCKER_USERNAME and DOCKER_PASSWORD
    Check disk space for image building

General Debugging#

# Describe a pod for events
kubectl
 describe pod <pod-name>

# Get all resources
kubectl
 get all

# Check events
kubectl
 get events --sort-by='.lastTimestamp'

Library Mode#

For teams preferring pure Python syntax or integrating Jac into existing Python codebases, Library Mode provides an alternative deployment approach. Instead of .jac files, you use Python files with Jac's runtime as a library.

    Complete Guide: See Library Mode for the full API reference, code examples, and migration guide.

Key Features:

    All Jac features accessible through jaclang.lib imports
    Pure Python syntax with decorators (@on_entry, @on_exit)
    Full IDE/tooling support (autocomplete, type checking, debugging)
    Zero migration friction for existing Python projects

Quick Example:

from jaclang.lib import Node, Walker, spawn, root, on_entry

class Task(Node):
    
title: str
    
done: bool = False

class TaskFinder(Walker):
    
@on_entry
    
def find(self, here: Task) -> None:
        
print(f"Found: {here.title}")

spawn(TaskFinder(), root())

Related Resources#

    Local API Server Tutorial
    Kubernetes Deployment Tutorial
    Backend Integration Tutorial

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
CLI Commands
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
            CLI Commands
            Configuration
            Code Organization
            Testing
            Debugging
        Python Integration
        Quick Reference

Table of contents

    Quick Reference
    Version Info
    Core Commands
        jac run
        jac start
        jac create
        jac check
        jac test
        jac format
        jac lint
        jac enter
    Visualization & Debug
        jac dot
        jac debug
            VS Code Debugger Setup
            Graph Visualization (jacvis)
    Plugin Management
        jac plugins
    Configuration Management
        jac config
    Deployment (jac-scale)
        jac start --scale
        jac status
        jac destroy
    Package Management
        jac add
        jac install
        jac remove
        jac update
        jac clean
        jac purge
    Template Management
        jac jacpack
        jac js
    Utility Commands
        jac grammar
        jac script
        jac py2jac
        jac jac2py
        jac tool
        jac nacompile
        jac completions
        jac lsp
    Plugin Commands
        jac-client Commands
            jac build
            jac setup
            Extended Flags
    Common Workflows
        Development
        Production
    See Also

    Full Reference
    Developer Workflow

CLI Reference#

The Jac CLI provides commands for running, building, testing, and deploying Jac applications.

    💡 Enhanced Output: For beautiful, colorful terminal output with Rich formatting, install the optional jac-super plugin: pip install jac-super. All CLI commands will automatically use enhanced output with themes, panels, and spinners.

Quick Reference#
Command 	Description
jac run 	Execute a Jac file
jac start 	Start REST API server (use --scale for K8s deployment)
jac create 	Create new project
jac check 	Type check code
jac test 	Run tests
jac format 	Format code
jac clean 	Clean project build artifacts
jac purge 	Purge global bytecode cache (works even if corrupted)
jac enter 	Run specific entrypoint
jac dot 	Generate graph visualization
jac debug 	Interactive debugger
jac plugins 	Manage plugins
jac config 	Manage project configuration
jac destroy 	Remove Kubernetes deployment (jac-scale)
jac status 	Show deployment status of Kubernetes resources (jac-scale)
jac add 	Add packages to project
jac install 	Install project dependencies
jac remove 	Remove packages from project
jac update 	Update dependencies to latest compatible versions
jac jacpack 	Manage project templates (.jacpack files)
jac grammar 	Extract and print the Jac grammar
jac script 	Run project scripts
jac py2jac 	Convert Python to Jac
jac jac2py 	Convert Jac to Python
jac tool 	Language tools (IR, AST)
jac lsp 	Language server
jac js 	JavaScript output
jac build 	Build for target platform (jac-client)
jac setup 	Setup build target (jac-client)
Version Info#

jac
 --version

Displays the Jac version, Python version, platform, and all detected plugins with their versions:

 _
(_) __ _  ___     Jac Language
| |/ _` |/ __|
| | (_| | (__     Version:  0.10.2
_/ |\__,_|\___|    Python 3.12.3
|__/                Platform: Linux x86_64

🔌 Plugins Detected:
   byllm==0.4.17
   jac-client==0.2.13
   jac-scale==0.1.4
   jac-super==0.1.0

Core Commands#
jac run#

Execute a Jac file.

Note: jac <file> is shorthand for jac run <file> - both work identically.

jac
 run [-h] [-m] [--no-main] [-c] [--no-cache] [--profile PROFILE] filename [args ...]

Option 	Description 	Default
filename 	Jac file to run 	Required
-m, --main 	Treat module as __main__ 	True
-c, --cache 	Enable compilation cache 	True
--profile 	Configuration profile to load (e.g. prod, staging) 	""
args 	Arguments passed to the script (available via sys.argv[1:]) 	

Like Python, everything after the filename is passed to the script. Jac flags must come before the filename.

Examples:

# Run a file
jac
 run main.jac

# Run without cache (flags before filename)
jac
 run --no-cache main.jac

# Pass arguments to the script
jac
 run script.jac arg1 arg2

# Pass flag-like arguments to the script
jac
 run script.jac --verbose --output result.txt

Passing arguments to scripts:

Arguments after the filename are available in the script via sys.argv:

# greet.jac
import sys;

with entry {
    
name = sys.argv[1] if len(sys.argv) > 1 else "World";
    
print(f"Hello, {name}!");
}

jac
 run greet.jac Alice        # Hello, Alice!
jac
 run greet.jac              # Hello, World!

sys.argv[0] is the script filename (like Python). For scripts that accept flags, use Python's argparse module:

import argparse;

with entry {
    
parser = argparse.ArgumentParser();
    
parser.add_argument("--name", default="World");
    
args = parser.parse_args();
    
print(f"Hello, {args.name}!");
}

jac
 run greet.jac --name Alice

jac start#

Start a Jac application as an HTTP API server. With the jac-scale plugin installed, use --scale to deploy to Kubernetes. Use --dev for Hot Module Replacement (HMR) during development.

jac
 start [-h] [-p PORT] [-m] [--no-main] [-f] [--no-faux] [-d] [--no-dev] [-a API_PORT] [-n] [--no-no_client] [--scale] [--no-scale] [-b] [--no-build] [filename]

Option 	Description 	Default
filename 	Jac file to serve 	main.jac
-p, --port 	Port number 	8000
-m, --main 	Treat as __main__ 	True
-f, --faux 	Print docs only (no server) 	False
-d, --dev 	Enable HMR (Hot Module Replacement) mode 	False
--api_port 	Separate API port for HMR mode (0=same as port) 	0
--no_client 	Skip client bundling/serving (API only) 	False
--scale 	Deploy to Kubernetes (requires jac-scale) 	False
-b, --build 	Build Docker image before deploy (with --scale) 	False

Examples:

# Start with default main.jac on default port
jac
 start

# Start on custom port
jac
 start -p 3000

# Start with Hot Module Replacement (development)
jac
 start --dev

# HMR mode without client bundling (API only)
jac
 start --dev --no-client

# Deploy to Kubernetes (requires jac-scale plugin)
jac
 start --scale

# Build and deploy to Kubernetes
jac
 start --scale --build

    Note:

        If your project uses a different entry file (e.g., app.jac, server.jac), you can specify it explicitly: jac start app.jac

jac create#

Initialize a new Jac project with configuration. Creates a project folder with the given name containing the project files.

jac
 create [-h] [-f] [-u USE] [-l] [name]

Option 	Description 	Default
name 	Project name (creates folder with this name) 	Current directory name
-f, --force 	Overwrite existing project 	False
-u, --use 	Jacpac template: registered name, file path, or URL 	default
-l, --list-jacpacks 	List available jacpack templates 	False

Examples:

# Create basic project (creates myapp/ folder)
jac
 create myapp
cd myapp

# Create full-stack project with client template (requires jac-client)
jac
 create myapp --use client

# Create from a local .jacpack file
jac
 create myapp --use ./my-template.jacpack

# Create from a local template directory
jac
 create myapp --use ./my-template/

# Create from a URL
jac
 create myapp --use https://example.com/template.jacpack

# List available jacpack templates
jac
 create --list-jacpacks

# Force overwrite existing
jac
 create myapp --force

# Create in current directory
jac
 create

See Also: Use jac jacpack to create and bundle custom templates.
jac check#

Type check Jac code for errors.

jac
 check [-h] [-e] [-w] [--ignore PATTERNS] [-p] [--nowarn] paths [paths ...]

Option 	Description 	Default
paths 	Files/directories to check 	Required
-e, --print_errs 	Print detailed error messages 	True
-w, --warnonly 	Treat errors as warnings 	False
--ignore 	Comma-separated list of files/folders to ignore 	None
-p, --parse_only 	Only check syntax (skip type checking) 	False
--nowarn 	Suppress warning output 	False

Examples:

# Check a file
jac
 check main.jac

# Check a directory
jac
 check src/

# Warnings only mode
jac
 check main.jac -w

# Check directory excluding specific folders/files
jac
 check myproject/ --ignore fixtures tests

# Check excluding multiple patterns
jac
 check . --ignore node_modules dist __pycache__

jac test#

Run tests in Jac files.

jac
 test [-h] [-t TEST_NAME] [-f FILTER] [-x] [-m MAXFAIL] [-d DIRECTORY] [-v] [filepath]

Option 	Description 	Default
filepath 	Test file to run 	None
-t, --test_name 	Specific test name 	None
-f, --filter 	Filter tests by pattern 	None
-x, --xit 	Exit on first failure 	False
-m, --maxfail 	Max failures before stop 	None
-d, --directory 	Test directory 	None
-v, --verbose 	Verbose output 	False

Examples:

# Run all tests in a file
jac
 test main.jac

# Run tests in directory
jac
 test -d tests/

# Run specific test
jac
 test main.jac -t my_test

# Stop on first failure
jac
 test main.jac -x

# Verbose output
jac
 test main.jac -v

jac format#

Format Jac code according to style guidelines. For auto-linting (code corrections like combining consecutive has statements, converting @staticmethod to static), use jac lint --fix instead.

jac
 format [-h] [-s] [-l] [-c] paths [paths ...]

Option 	Description 	Default
paths 	Files/directories to format 	Required
-s, --to_screen 	Print to stdout instead of writing 	False
-l, --lintfix 	Also apply auto-lint fixes in the same pass 	False
-c, --check 	Check if files are formatted without modifying them (exit 1 if unformatted) 	False

Examples:

# Preview formatting
jac
 format main.jac -s

# Apply formatting
jac
 format main.jac

# Format entire directory
jac
 format .

# Check formatting without modifying (useful in CI)
jac
 format . --check

    Note: For auto-linting (code corrections), use jac lint --fix instead. See jac lint below.

jac lint#

Lint Jac files and report violations. Use --fix to auto-fix violations.

jac
 lint [-h] [-f] [--ignore IGNORE] paths [paths ...]

Option 	Description 	Default
paths 	Files/directories to lint 	Required
-f, --fix 	Auto-fix lint violations 	False
--ignore 	Comma-separated files/folders to ignore 	""

Examples:

# Report lint violations
jac
 lint main.jac

# Auto-fix violations
jac
 lint main.jac --fix

# Lint entire directory
jac
 lint .

# Lint excluding folders
jac
 lint . --ignore fixtures

    Lint Rules: Configure rules via [check.lint] in jac.toml. All enabled rules are treated as errors.

jac enter#

Run a specific entrypoint in a Jac file.

jac
 enter [-h] [-m] [-r ROOT] [-n NODE] filename entrypoint [args ...]

Option 	Description 	Default
filename 	Jac file 	Required
entrypoint 	Function/walker to invoke (positional) 	Required
args 	Arguments to pass 	None
-m, --main 	Treat as __main__ 	True
-r, --root 	Root executor ID 	None
-n, --node 	Starting node ID 	None

Examples:

# Run specific entrypoint
jac
 enter main.jac my_walker

# With arguments
jac
 enter main.jac process_data arg1 arg2

# With root and node
jac
 enter main.jac my_walker -r root_id -n node_id

Visualization & Debug#
jac dot#

Generate DOT graph visualization.

jac
 dot [-h] [-s SESSION] [-i INITIAL] [-d DEPTH] [-t] [-b] [-e EDGE_LIMIT] [-n NODE_LIMIT] [-o SAVETO] [-p] [-f FORMAT] filename [connection ...]

Option 	Description 	Default
filename 	Jac file 	Required
-s, --session 	Session identifier 	None
-i, --initial 	Initial node ID 	None
-d, --depth 	Max traversal depth 	-1 (unlimited)
-t, --traverse 	Enable traversal mode 	False
-c, --connection 	Connection filters 	None
-b, --bfs 	Use BFS traversal 	False
-e, --edge_limit 	Max edges 	512
-n, --node_limit 	Max nodes 	512
-o, --saveto 	Output file path 	None
-p, --to_screen 	Print to stdout 	False
-f, --format 	Output format 	dot

Examples:

# Generate DOT output
jac
 dot main.jac -s my_session --to_screen

# Save to file
jac
 dot main.jac -s my_session --saveto graph.dot

# Limit depth
jac
 dot main.jac -s my_session -d 3

jac debug#

Start interactive debugger.

jac
 debug [-h] [-m] [-c] filename

Option 	Description 	Default
filename 	Jac file to debug 	Required
-m, --main 	Run main entry 	True
-c, --cache 	Use cache 	False

Examples:

# Start debugger
jac
 debug main.jac

VS Code Debugger Setup#

To use the VS Code debugger with Jac:

    Install the Jac extension from the VS Code Extensions marketplace
    Enable Debug: Allow Breakpoints Everywhere in VS Code Settings (search "breakpoints")
    Create a launch.json via Run and Debug panel (Ctrl+Shift+D) → "Create a launch.json file" → select "Jac Debug"

The generated .vscode/launch.json:

{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "jac",
            "request": "launch",
            "name": "Jac Debug",
            "program": "${file}"
        }
    ]
}

Debugger controls: F5 (continue), F10 (step over), F11 (step into), Shift+F11 (step out).
Graph Visualization (jacvis)#

The Jac extension includes live graph visualization:

    Open VS Code Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
    Type jacvis and select jacvis: Visualize Jaclang Graph
    A side panel opens showing your graph structure

Set breakpoints and step through code -- nodes and edges appear in real time as your program builds the graph. Open jacvis before starting the debugger for best results.

For a complete walkthrough, see the Debugging in VS Code Tutorial.
Plugin Management#
jac plugins#

Manage Jac plugins.

jac
 plugins [-h] [-v] [action] [names ...]

Action 	Description
list 	List installed plugins (default)
info 	Show plugin information
enable 	Enable plugins
disable 	Disable plugins
disabled 	List disabled plugins
Option 	Description 	Default
-v, --verbose 	Verbose output 	False

Examples:

# List plugins (action defaults to 'list')
jac
 plugins

# Explicitly list plugins
jac
 plugins list

# Show info about a plugin
jac
 plugins info byllm

# Disable a plugin
jac
 plugins disable byllm

# Enable a plugin
jac
 plugins enable byllm

# List disabled plugins
jac
 plugins disabled

    Note: To install or uninstall plugins, use pip install / pip uninstall directly. The jac plugins command manages enabled/disabled state for already-installed plugins.

    💡 Popular Plugins:

        jac-super: Enhanced console output with Rich formatting, colors, and spinners (pip install jac-super)
        jac-client: Full-stack web development with client-side rendering (pip install jac-client)
        jac-scale: Kubernetes deployment and scaling (pip install jac-scale)

Configuration Management#
jac config#

View and modify project configuration settings in jac.toml.

jac
 config [action] [key] [value] [-g GROUP] [-o FORMAT]

Action 	Description
show 	Display explicitly set configuration values (default)
list 	Display all settings including defaults
get 	Get a specific setting value
set 	Set a configuration value
unset 	Remove a configuration value (revert to default)
path 	Show path to config file
groups 	List available configuration groups
Option 	Description 	Default
key 	Configuration key (positional, e.g., project.name) 	None
value 	Value to set (positional) 	None
-g, --group 	Filter by configuration group 	None
-o, --output 	Output format (table, json, toml) 	table

Configuration Groups:

    project - Project metadata (name, version, description)
    run - Runtime settings (cache, session)
    build - Build settings (typecheck, output directory)
    test - Test settings (verbose, filters)
    serve - Server settings (port, host)
    format - Formatting options
    check - Type checking options
    dot - Graph visualization settings
    cache - Cache configuration
    plugins - Plugin management
    environment - Environment variables

Examples:

# Show explicitly set configuration
jac
 config show

# Show all settings including defaults
jac
 config list

# Show settings for a specific group
jac
 config show -g project

# Get a specific value
jac
 config get project.name

# Set a value
jac
 config set project.version "2.0.0"

# Remove a value (revert to default)
jac
 config unset run.cache

# Show config file path
jac
 config path

# List available groups
jac
 config groups

# Output as JSON
jac
 config show -o json

# Output as TOML
jac
 config list -o toml

Deployment (jac-scale)#
jac start --scale#

Deploy to Kubernetes using the jac-scale plugin. See the jac start command above for full options.

jac
 start --scale           # Deploy without building
jac
 start --scale --build   # Build and deploy

jac status#

Show the deployment status of your Jac application on Kubernetes. Displays a color-coded table with the health of each component (application, Redis, MongoDB, Prometheus, Grafana), pod readiness counts, and service URLs.

jac
 status [-h] file_path [--target TARGET]

Option 	Description 	Default
file_path 	Path to the .jac file 	Required
--target 	Deployment target platform 	kubernetes

Example output:

  Jac Scale - Deployment Status
  App: my-app   Namespace: default

┌───────────────────┬────────────────────────┬───────┐
│ Component         │ Status                 │ Pods  │
├───────────────────┼────────────────────────┼───────┤
│ Jaseci App        │ ● Running              │  1/1  │
│ Redis             │ ● Running              │  1/1  │
│ MongoDB           │ ● Running              │  1/1  │
│ Prometheus        │ ● Running              │  1/1  │
│ Grafana           │ ● Running              │  1/1  │
└───────────────────┴────────────────────────┴───────┘

  Service URLs
  ────────────────────────────────────────────
  Application:  http://localhost:30001
  Grafana:      http://localhost:30003

Status indicators:
Symbol 	Meaning
● Running 	All pods healthy and ready
◑ Degraded 	Some pods ready, but not all
⟳ Pending 	Pods are starting up
↺ Restarting 	Pods are crash-looping
✗ Failed 	Component has failed
○ Not Deployed 	Component is not present in the cluster

Examples:

# Check deployment status
jac
 status app.jac

# Check status with explicit target
jac
 status app.jac --target kubernetes

jac destroy#

Remove a deployment.

jac
 destroy [-h] file_path

Option 	Description 	Default
file_path 	Jac file to undeploy 	Required

Examples:

jac
 destroy main.jac

Package Management#
jac add#

Add packages to your project's dependencies. Requires at least one package argument (use jac install to install all existing dependencies). When no version is specified, the package is installed unconstrained and then the installed version is queried to record a ~=X.Y compatible-release spec in jac.toml.

jac
 add [-h] [-d] [-g GIT] [-v] [packages ...]

Option 	Description 	Default
packages 	Package specifications (required) 	None
-d, --dev 	Add as dev dependency 	False
-g, --git 	Git repository URL 	None
-v, --verbose 	Show detailed output 	False

With jac-client plugin:
Option 	Description 	Default
--npm 	Add as client-side (npm) package 	False

Examples:

# Add a package (records ~=2.32 based on installed version)
jac
 add requests

# Add with explicit version constraint
jac
 add "numpy>=1.24"

# Add multiple packages
jac
 add numpy pandas scipy

# Add as dev dependency
jac
 add pytest --dev

# Add from git repository
jac
 add --git https://github.com/user/package.git

# Add npm package (requires jac-client)
jac
 add react --npm

For private packages from custom registries (e.g., GitHub Packages), configure scoped registries and auth tokens in jac.toml under [plugins.client.npm]. See NPM Registry Configuration.
jac install#

Sync the project environment to jac.toml. Installs all Python (pip), git, and plugin-provided (npm, etc.) dependencies in one command. Creates or validates the project virtual environment at .jac/venv/.

jac
 install [-h] [-d] [-v]

Option 	Description 	Default
-d, --dev 	Include dev dependencies 	False
-v, --verbose 	Show detailed output 	False

Examples:

# Install all dependencies
jac
 install

# Install including dev dependencies
jac
 install --dev

# Install with verbose output
jac
 install -v

jac remove#

Remove packages from your project's dependencies.

jac
 remove [-h] [-d] [packages ...]

Option 	Description 	Default
packages 	Package names to remove 	None
-d, --dev 	Remove from dev dependencies 	False

With jac-client plugin:
Option 	Description 	Default
--npm 	Remove client-side (npm) package 	False

Examples:

# Remove a package
jac
 remove requests

# Remove multiple packages
jac
 remove numpy pandas

# Remove dev dependency
jac
 remove pytest --dev

# Remove npm package (requires jac-client)
jac
 remove react --npm

jac update#

Update dependencies to their latest compatible versions. For each updated package, the installed version is queried and a ~=X.Y compatible-release spec is written back to jac.toml.

jac
 update [-h] [-d] [-v] [packages ...]

Option 	Description 	Default
packages 	Specific packages to update (all if empty) 	None
-d, --dev 	Include dev dependencies 	False
-v, --verbose 	Show detailed output 	False

Examples:

# Update all dependencies to latest compatible versions
jac
 update

# Update a specific package
jac
 update requests

# Update all including dev dependencies
jac
 update --dev

jac clean#

Clean project build artifacts from the .jac/ directory.

jac
 clean [-h] [-a] [-d] [-c] [-p] [-f]

Option 	Description 	Default
-a, --all 	Clean all .jac artifacts (data, cache, packages, client) 	False
-d, --data 	Clean data directory (.jac/data) 	False
-c, --cache 	Clean cache directory (.jac/cache) 	False
-p, --packages 	Clean virtual environment (.jac/venv) 	False
-f, --force 	Force clean without confirmation prompt 	False

By default (no flags), jac clean removes only the data directory (.jac/data).

Examples:

# Clean data directory (default)
jac
 clean

# Clean all build artifacts
jac
 clean --all

# Clean only cache
jac
 clean --cache

# Clean data and cache directories
jac
 clean --data --cache

# Force clean without confirmation
jac
 clean --all --force

    💡 Troubleshooting Tip: If you encounter unexpected syntax errors, "NodeAnchor is not a valid reference" errors, or other strange behavior after modifying your code, try clearing the cache with jac clean --cache (rm -rf .jac) or jac purge. Stale bytecode can cause issues when source files change.

jac purge#

Purge the global bytecode cache. Works even when the cache is corrupted.

jac
 purge

When to use:

    After upgrading Jaseci packages
    When encountering cache-related errors (jaclang.pycore, NodeAnchor, etc.)
    When setup stalls during first-time compilation

Command 	Scope
jac clean --cache 	Local project (.jac/cache/)
jac purge 	Global system cache
Template Management#
jac jacpack#

Manage project templates. Bundle template directories into distributable .jacpack files or list available templates.

jac
 jacpack [action] [path] [-o OUTPUT]

Action 	Description
pack 	Bundle a template directory into a .jacpack file
list 	List available templates (default)
info 	Show information about a template
Option 	Description 	Default
path 	Template directory (for pack) or .jacpack file (for info) 	None
-o, --output 	Output file path for bundled template 	<name>.jacpack

Template Directory Structure:

A template directory should contain:

    jac.toml - Project config with a [jacpack] section for metadata
    Template files (.jac, .md, etc.) with {{name}} placeholders

To make any Jac project packable as a template, simply add a [jacpack] section to your jac.toml. All other sections become the config for created projects.

Example jac.toml for a template:

# Standard project config (becomes the created project's jac.toml)
[project]
name = "{{name}}"
version = "0.1.0"
entry-point = "main.jac"

[dependencies]

# Jacpac metadata - used when packing, stripped from created projects
[jacpack]
name = "mytemplate"
description = "My custom project template"
jaclang = "0.9.0"

[[jacpack.plugins]]
name = "jac-client"
version = "0.1.0"

[jacpack.options]
directories = [".jac"]
root_gitignore_entries = [".jac/"]

Examples:

# List available templates
jac
 jacpack list

# Bundle a template directory
jac
 jacpack pack ./my-template

# Bundle with custom output path
jac
 jacpack pack ./my-template -o custom-name.jacpack

# Show template info
jac
 jacpack info ./my-template
jac
 jacpack info mytemplate.jacpack

Using Templates with jac create:

Once a template is registered, use it with the --use flag:

jac
 create myproject --use mytemplate

jac js#

Generate JavaScript output from Jac code (used for jac-client frontend compilation).

jac
 js [-h] filename

Option 	Description 	Default
filename 	Jac file to compile to JS 	Required

Examples:

# Generate JS from Jac file
jac
 js app.jac

Utility Commands#
jac grammar#

Extract and print the Jac grammar.

jac
 grammar [-h] [--lark] [-o OUTPUT]

Option 	Description 	Default
--lark 	Output in Lark format instead of EBNF 	False
-o, --output 	Write output to file instead of stdout 	None

Examples:

# Print grammar in EBNF format
jac
 grammar

# Print in Lark format
jac
 grammar --lark

# Save to file
jac
 grammar -o grammar.ebnf

jac script#

Run custom scripts defined in the [scripts] section of jac.toml.

jac
 script [-h] [-l] [name]

Option 	Description 	Default
name 	Script name to run 	None
-l, --list_scripts 	List available scripts 	False

Examples:

# Run a script
jac
 script dev

# List available scripts
jac
 script --list

See Configuration: Scripts for defining scripts in jac.toml.
jac py2jac#

Convert Python code to Jac.

jac
 py2jac filename

Examples:

jac
 py2jac script.py

jac jac2py#

Convert Jac code to Python.

jac
 jac2py filename

Examples:

jac
 jac2py main.jac

jac tool#

Access language tools (IR, AST, etc.).

jac
 tool tool [args ...]

Available tools:

# View IR options
jac
 tool ir

# View AST
jac
 tool ir ast main.jac

# View symbol table
jac
 tool ir sym main.jac

# View generated Python
jac
 tool ir py main.jac

jac nacompile#

Compile a .na.jac file to a standalone native ELF executable. No external compiler, assembler, or linker is required. The entire pipeline runs in pure Python using llvmlite and a built-in ELF linker.

jac
 nacompile filename [-o OUTPUT]

Option 	Description 	Default
filename 	Path to the .na.jac file (must have with entry {} block) 	required
-o, --output 	Output binary path 	filename without .na.jac

The file must contain a with entry { } block (which defines the jac_entry() function). Files with Python/server dependencies (native_imports) cannot be compiled to standalone binaries.

What happens under the hood:

    Compiles the .na.jac through the Jac pipeline to get LLVM IR
    Injects main() and _start as pure LLVM IR (zero inline assembly)
    Emits native object code via llvmlite's emit_object()
    Links into an ELF executable via the built-in pure-Python ELF linker

The resulting binary dynamically links against libc.so.6. Memory management uses a self-contained reference counting scheme -- no external garbage collector (libgc) is required.

Examples:

# Compile to ./chess
jac
 nacompile chess.na.jac

# Compile with custom output name
jac
 nacompile chess.na.jac -o mychess

# Run the binary
./mychess

jac completions#

Generate and install shell completion scripts for the jac CLI.

jac
 completions [-h] [-s SHELL] [-i] [--no-install]

Option 	Description 	Default
-s, --shell 	Shell type (bash, zsh, fish) 	bash
-i, --install 	Auto-install completion to shell config 	False

When --install is used, the completion script is written to ~/.jac/completions.<shell> (e.g. ~/.jac/completions.bash) and a source line is added to your shell config file (~/.bashrc, ~/.zshrc, or ~/.config/fish/config.fish).

Installed files:
Shell 	Completion script 	Config modified
bash 	~/.jac/completions.bash 	~/.bashrc
zsh 	~/.jac/completions.zsh 	~/.zshrc
fish 	~/.jac/completions.fish 	~/.config/fish/config.fish

Examples:

# Print bash completion script to stdout
jac
 completions

# Auto-install for bash (writes to ~/.jac/completions.bash)
jac
 completions --install

# Generate zsh completions
jac
 completions --shell zsh

# Auto-install for fish
jac
 completions --shell fish --install

    Note: After installing, run source ~/.bashrc (or restart your shell) to activate completions. Completions cover subcommands, options, and file paths.

jac lsp#

Start the Language Server Protocol server (for IDE integration).

jac
 lsp

Plugin Commands#

Plugins can add new commands and extend existing ones. These commands are available when the corresponding plugin is installed.
jac-client Commands#

Requires: pip install jac-client
jac build#

Build a Jac application for a specific target.

jac
 build [filename] [--client TARGET] [-p PLATFORM]

Option 	Description 	Default
filename 	Path to .jac file 	main.jac
--client 	Build target (web, desktop) 	web
-p, --platform 	Desktop platform (windows, macos, linux, all) 	Current platform

Examples:

# Build web target (default)
jac
 build

# Build desktop app
jac
 build --client desktop

# Build for Windows
jac
 build --client desktop --platform windows

jac setup#

One-time initialization for a build target.

jac
 setup <target>

Examples:

# Setup Tauri for desktop builds
jac
 setup desktop

Extended Flags#
Base Command 	Added Flag 	Description
jac create 	--use client 	Create full-stack project template
jac create 	--skip 	Skip npm package installation
jac start 	--client <target> 	Client build target for dev server
jac add 	--npm 	Add npm (client-side) dependency
jac remove 	--npm 	Remove npm (client-side) dependency
Common Workflows#
Development#

# Create project
jac
 create myapp
cd myapp

# Run
jac
 run main.jac

# Test
jac
 test -v

# Lint and fix
jac
 lint . --fix

Production#

# Start locally
jac
 start -p 8000

# Deploy to Kubernetes
jac
 start main.jac --scale

# Check deployment status
jac
 status main.jac

# Remove deployment
jac
 destroy main.jac

See Also#

    Project Configuration
    jac-scale Documentation
    Testing Guide

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Configuration
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
            CLI Commands
            Configuration
            Code Organization
            Testing
            Debugging
        Python Integration
        Quick Reference

Table of contents

    Creating a Project
    Configuration Sections
        [project]
        [dependencies]
        [run]
        [serve]
        [build]
        [test]
        [format]
        [check]
            [check.lint]
        [dot]
        [cache]
        [storage]
        [plugins]
        [scripts]
        [environments]
    Environment Variables
    CLI Override
    Complete Example
    .jacignore
        Format
    Environment Variables
        General
        Storage
        jac-scale: Database
        jac-scale: Authentication
        jac-scale: Webhooks
        jac-scale: Kubernetes
    See Also

    Full Reference
    Developer Workflow

Configuration Reference#

The jac.toml file is the central configuration for Jac projects. It defines project metadata, dependencies, command defaults, and plugin settings.
Creating a Project#

# Basic project
jac
 create myapp
cd myapp

# Full-stack web app (recommended for web development)
jac
 create myapp --use client
cd myapp

This creates a jac.toml with default settings. When using --use client, the scaffolded project includes:

myapp/
├── main.jac       # Entry point with server and client code
├── jac.toml       # Project configuration (auto-generated)
└── styles.css     # Default stylesheet

The auto-generated jac.toml for a --use client project looks like:

[project]
name = "myapp"
version = "0.0.1"
entry-point = "main.jac"

You typically don't need to modify this file until you add dependencies or customize settings.
Configuration Sections#
[project]#

Project metadata:

[project]
name = "myapp"
version = "1.0.0"
description = "My Jac application"
authors = ["Your Name <you@example.com>"]
license = "MIT"
entry-point = "main.jac"
jac-version = ">=0.9.0"

[project.urls]
homepage = "https://example.com"
repository = "https://github.com/user/repo"

Field 	Description
name 	Project name (required)
version 	Semantic version
description 	Brief description
authors 	List of authors
license 	License identifier
entry-point 	Main file (default: main.jac)
jac-version 	Required Jac version
[dependencies]#

Python/PyPI packages and Jac plugins:

[dependencies]
requests = ">=2.28.0"
numpy = "1.24.0"
byllm = ">=0.4.8"

[dev-dependencies]
pytest = ">=8.0.0"

[dependencies.git]
my-lib = { git = "https://github.com/user/repo.git", branch = "main" }

Version specifiers:
Format 	Example 	Meaning
Exact 	"1.0.0" 	Exactly 1.0.0
Minimum 	">=1.0.0" 	1.0.0 or higher
Range 	">=1.0,<2.0" 	1.x only
Compatible 	"~=1.4.2" 	1.4.x

    Default behavior: When you run jac add requests without a version, the package is installed unconstrained and then the actual installed version is queried. A compatible-release spec (~=X.Y) is recorded -- e.g., if pip installs 2.32.5, jac.toml gets requests = "~=2.32". The jac update command also uses this format when writing updated versions back.

[run]#

Defaults for jac run:

[run]
session = ""        # Session name for persistence
main = true         # Run as main module
cache = true        # Use bytecode cache

[serve]#

Defaults for jac start:

[serve]
port = 8000              # Server port
session = ""             # Session name
main = true              # Run as main module
cl_route_prefix = "cl"   # URL prefix for client apps
base_route_app = ""      # Client app to serve at /

[build]#

Build configuration:

[build]
typecheck = false   # Enable type checking
dir = ".jac"        # Build artifacts directory

The dir setting controls where all build artifacts are stored:

    .jac/cache/ - Bytecode cache
    .jac/venv/ - Project virtual environment
    .jac/client/ - Client-side builds
    .jac/data/ - Runtime data

[test]#

Defaults for jac test:

[test]
directory = ""          # Test directory (empty = current directory)
filter = ""             # Filter pattern
verbose = false         # Verbose output
fail_fast = false       # Stop on first failure
max_failures = 0        # Max failures (0 = unlimited)

[format]#

Defaults for jac format:

[format]
outfile = ""        # Output file (empty = in-place)

[check]#

Defaults for jac check:

[check]
print_errs = true   # Print errors to console
warnonly = false     # Treat errors as warnings

[check.lint]#

Configure which auto-lint rules are active during jac lint and jac lint --fix. Rules use a select/ignore model with two group keywords:

    "default" - code-transforming rules only (safe, auto-fixable)
    "all" - every rule, including unfixable rules like no-print

[check.lint]
select = ["default"]          # Code-transforming rules only (default)
ignore = ["combine-has"]      # Disable specific rules
exclude = []                  # File patterns to skip (glob syntax)

To enable all rules including warning-only rules:

[check.lint]
select = ["all"]              # Everything, including no-print

To add specific rules on top of defaults:

[check.lint]
select = ["default", "no-print"]  # Defaults + no-print warnings

To enable only specific rules:

[check.lint]
select = ["combine-has", "remove-empty-parens"]

Available lint rules:
Rule Name 	Description 	Group
combine-has 	Combine consecutive has statements with same modifiers 	default
combine-glob 	Combine consecutive glob statements with same modifiers 	default
staticmethod-to-static 	Convert @staticmethod decorator to static keyword 	default
init-to-can 	Convert def __init__ / def __post_init__ to can init / can postinit 	default
remove-empty-parens 	Remove empty parentheses from declarations (def foo() → def foo) 	default
remove-kwesc 	Remove unnecessary backtick escaping from non-keyword names 	default
hasattr-to-null-ok 	Convert hasattr(obj, "attr") to null-safe access (obj?.attr) 	default
simplify-ternary 	Simplify x if x else default to x or default 	default
remove-future-annotations 	Remove import from __future__ { annotations } (not needed in Jac) 	default
fix-impl-signature 	Fix signature mismatches between declarations and implementations 	default
remove-import-semi 	Remove trailing semicolons from import from X { ... } 	default
no-print 	Error on bare print() calls (use console abstraction instead) 	all

Excluding files from lint:

Use exclude to skip files matching glob patterns:

[check.lint]
select = ["all"]
exclude = [
    "docs/*",
    "*/examples/*",
    "*/tests/*",
    "legacy_module.jac",
]

Patterns are matched against file paths relative to the project root. Use * for single-directory wildcards and ** for recursive matching.
[dot]#

Defaults for jac dot (graph visualization):

[dot]
depth = -1          # Traversal depth (-1 = unlimited)
traverse = false    # Traverse connections
bfs = false         # Use BFS (default: DFS)
edge_limit = 512    # Maximum edges
node_limit = 512    # Maximum nodes
format = "dot"      # Output format

[cache]#

Bytecode cache settings:

[cache]
enabled = true      # Enable caching
dir = ".jac_cache"  # Cache directory

[storage]#

Plugin-Specific Configuration

The [storage] section requires the jac-scale plugin and may not be available in all configurations. Running jac config list -g storage will return "Unknown group 'storage'" if the plugin is not installed.

File storage configuration:

[storage]
storage_type = "local"       # Storage backend (local)
base_path = "./storage"      # Base directory for files
create_dirs = true           # Auto-create directories

Field 	Description 	Default
storage_type 	Storage backend type 	"local"
base_path 	Base directory for file storage 	"./storage"
create_dirs 	Automatically create directories 	true

Environment Variable Overrides:
Variable 	Description
JAC_STORAGE_TYPE 	Storage type (overrides config)
JAC_STORAGE_PATH 	Base directory (overrides config)
JAC_STORAGE_CREATE_DIRS 	Auto-create directories ("true"/"false")

Configuration priority: jac.toml > environment variables > defaults.

See Storage Reference for the full storage API.
[plugins]#

Plugin configuration:

[plugins]
discovery = "auto"      # "auto", "manual", or "disabled"
enabled = ["byllm"] # Explicitly enabled
disabled = []           # Explicitly disabled

# Plugin-specific settings
[plugins.byllm]
model = "gpt-4"
temperature = 0.7
api_key = "${OPENAI_API_KEY}"

# Webhook settings (jac-scale)
[plugins.scale.webhook]
secret = "your-webhook-secret-key"
signature_header = "X-Webhook-Signature"
verify_signature = true
api_key_expiry_days = 365

# Kubernetes version pinning (jac-scale)
[plugins.scale.kubernetes.plugin_versions]
jaclang = "latest"
jac_scale = "latest"
jac_client = "latest"
jac_byllm = "none"           # Use "none" to skip installation

Prometheus Metrics (jac-scale):

[plugins.scale.metrics]
enabled = true
endpoint = "/metrics"
namespace = "myapp"
walker_metrics = true

See Prometheus Metrics for details.

Kubernetes Secrets (jac-scale):

[plugins.scale.secrets]
OPENAI_API_KEY = "${OPENAI_API_KEY}"
DATABASE_PASSWORD = "${DB_PASS}"

See Kubernetes Secrets for details.

See also jac-scale Webhooks and Kubernetes Deployment for more options.

Import Path Aliases (jac-client):

[plugins.client.paths]
"@components/*" = "./components/*"
"@utils/*" = "./utils/*"
"@shared" = "./shared/index"

Defines custom import aliases applied to Vite resolve.alias, TypeScript compilerOptions.paths, and the Jac module resolver. See jac-client Import Path Aliases for details.

NPM Registry Configuration (jac-client):

[plugins.client.npm.scoped_registries]
"@mycompany" = "https://npm.pkg.github.com"

[plugins.client.npm.auth."//npm.pkg.github.com/"]
_authToken = "${NODE_AUTH_TOKEN}"

This generates an .npmrc file during dependency installation for private/scoped npm packages. See jac-client NPM Registry Configuration for details.

Build-Time Constants (jac-client):

Define global variables that are replaced at compile time in client code via the [plugins.client.vite.define] section:

[plugins.client.vite.define]
"globalThis.API_URL" = "\"https://api.example.com\""
"globalThis.FEATURE_ENABLED" = true
"globalThis.BUILD_VERSION" = "\"1.2.3\""

These values are inlined by Vite during bundling. String values must be double-quoted (JSON-encoded). In client code, access them directly:

cl {
    
def:pub Footer() -> JsxElement {
        
return <p>Version: {globalThis.BUILD_VERSION}</p>;
    
}
}

[scripts]#

Custom command shortcuts:

[scripts]
dev = "jac run main.jac"
test = "jac test -v"
build = "jac build main.jac -t"
lint = "jac lint . --fix"
format = "jac format ."

Run with:

jac
 script dev
jac
 script test

[environments]#

Environment-specific overrides:

[environment]
default_profile = "development"

[environments.development]
[environments.development.run]
cache = false
[environments.development.plugins.byllm]
model = "gpt-3.5-turbo"

[environments.production]
inherits = "development"
[environments.production.run]
cache = true
[environments.production.plugins.byllm]
model = "gpt-4"

Activate a profile:

JAC_PROFILE=production jac run main.jac

Environment Variables#

Use environment variable interpolation:

[plugins.byllm]
api_key = "${OPENAI_API_KEY}"              # Required
model = "${MODEL:-gpt-3.5-turbo}"          # With default
secret = "${SECRET:?Secret is required}"   # Required with error

Syntax 	Description
${VAR} 	Use variable (error if not set)
${VAR:-default} 	Use default if not set
${VAR:?error} 	Custom error if not set
CLI Override#

Most settings can be overridden via CLI flags:

# Override run settings
jac
 run --no-cache --session my_session main.jac

# Override test settings
jac
 test --verbose --fail-fast

# Override serve settings
jac
 start --port 3000

Complete Example#

[project]
name = "my-ai-app"
version = "1.0.0"
description = "An AI-powered application"
entry-point = "main.jac"

[dependencies]
byllm = ">=0.4.8"
requests = ">=2.28.0"

[dev-dependencies]
pytest = ">=8.0.0"

[run]
main = true
cache = true

[serve]
port = 8000
cl_route_prefix = "cl"

[test]
directory = "tests"
verbose = true

[build]
typecheck = true
dir = ".jac"

[check.lint]
select = ["all"]
ignore = []
exclude = []

[plugins]
discovery = "auto"

[plugins.byllm]
model = "${LLM_MODEL:-gpt-4}"
api_key = "${OPENAI_API_KEY}"

[scripts]
dev = "jac run main.jac"
test = "jac test"
lint = "jac lint . --fix"

.jacignore#

The .jacignore file controls which Jac files are excluded from compilation and analysis. Place it in the project root.
Format#

One pattern per line, similar to .gitignore:

# Comments start with #
vite_client_bundle.impl.jac
test_fixtures/
*.generated.jac

Each line is a filename or pattern that should be skipped during Jac compilation passes (type checking, formatting, etc.).
Environment Variables#
General#
Variable 	Description
NO_COLOR 	Disable colored terminal output
NO_EMOJI 	Disable emoji in terminal output
JAC_PROFILE 	Activate a configuration profile (e.g., production)
JAC_BASE_PATH 	Override base directory for data/storage
Storage#
Variable 	Description
JAC_STORAGE_TYPE 	Storage backend type
JAC_STORAGE_PATH 	Base directory for file storage
JAC_STORAGE_CREATE_DIRS 	Auto-create directories
jac-scale: Database#
Variable 	Description
MONGODB_URI 	MongoDB connection URI
REDIS_URL 	Redis connection URL
jac-scale: Authentication#
Variable 	Description 	Default
JWT_SECRET 	Secret key for JWT signing 	supersecretkey
JWT_ALGORITHM 	JWT algorithm 	HS256
JWT_EXP_DELTA_DAYS 	Token expiration in days 	7
SSO_HOST 	SSO callback host URL 	http://localhost:8000/sso
SSO_GOOGLE_CLIENT_ID 	Google OAuth client ID 	None
SSO_GOOGLE_CLIENT_SECRET 	Google OAuth client secret 	None
jac-scale: Webhooks#
Variable 	Description
WEBHOOK_SECRET 	Secret for webhook HMAC signatures
WEBHOOK_SIGNATURE_HEADER 	Header name for signature
WEBHOOK_VERIFY_SIGNATURE 	Enable signature verification
WEBHOOK_API_KEY_EXPIRY_DAYS 	API key expiry in days
jac-scale: Kubernetes#
Variable 	Description 	Default
APP_NAME 	Application name for K8s resources 	jaseci
K8s_NAMESPACE 	Kubernetes namespace 	default
K8s_NODE_PORT 	External NodePort 	30001
K8s_CPU_REQUEST 	CPU resource request 	None
K8s_CPU_LIMIT 	CPU resource limit 	None
K8s_MEMORY_REQUEST 	Memory resource request 	None
K8s_MEMORY_LIMIT 	Memory resource limit 	None
DOCKER_USERNAME 	DockerHub username 	None
DOCKER_PASSWORD 	DockerHub password/token 	None
See Also#

    CLI Reference - Command-line interface documentation
    Plugin Management - Managing plugins

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Code Organization
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
            CLI Commands
            Configuration
            Code Organization
            Testing
            Debugging
        Python Integration
        Quick Reference

Table of contents

    Why Separate Declarations from Implementations?
        Architecture at a glance
        Readable by humans and AI models alike
        Granular separation of concerns
        Cleaner folder architecture
    Overview of Patterns
    Inline (All-in-One)
        What it looks like
        Real example
        When to use
    Side-by-Side Impl File (1:1)
        What it looks like
        Real example
        When to use
    Shared impl/ Directory (Many:Many)
        What it looks like
        Real example
        Where it's used in the compiler
        When to use
    .impl/ Directory (1:Many)
        What it looks like
        Real example
        When to use
    Pure Declarations (Data Modules)
        What it looks like
        When to use
    Choosing a Pattern
    Best Practices

    Full Reference
    Developer Workflow

Code Organization#

In most programming languages, the interface of a module -- what it exposes -- is interleaved with its implementation -- how it works. Jac takes a fundamentally different approach. Through its impl system, Jac allows you to cleanly separate declarations (the interfaces, types, and signatures that define a module's contract) from implementations (the method bodies and private helpers that fulfill that contract). As we will see throughout this guide, this distinction is far more than syntactic convenience -- it reshapes how both humans and AI models read, navigate, and reason about code.

In this guide, we will walk through the five organizational patterns used in the Jac compiler itself. For each pattern, we will examine when it is most appropriate, study real-world examples drawn from the compiler codebase, and discuss best practices for maintaining clarity and consistency as your projects grow.

Examples from the real compiler

Every example in this guide is drawn from the Jac compiler repository. These are not toy snippets -- they are the actual patterns used to build the language itself. Links point to the relevant source files so you can explore the full context on your own.

Prerequisites

This guide assumes you are already familiar with impl blocks and .impl.jac files. If you need a refresher, please review Implementations and Forward Declarations before continuing.
Why Separate Declarations from Implementations?#

Before diving into the patterns themselves, let us first understand why this separation matters. There are four key benefits worth examining closely.
Architecture at a glance#

When declarations live in their own files, every .jac file in a package reads like an API specification. You can open any declaration file and immediately see: what types exist, what fields they carry, what methods they expose, and what signatures those methods have -- all without wading through hundreds of lines of logic. The architecture of a system becomes visible from the file tree alone.

To illustrate this, consider the Jac compiler's type system:

compiler/type_system/
├── types.jac                  # What types exist in the type system
├── type_utils.jac             # What utility operations are available
├── type_evaluator.jac         # What the evaluator can do (256 lines of signatures)
├── operations.jac             # What type operations are supported
├── enum_utils.jac             # What enum helpers exist
└── impl/                      # How all of the above actually work

Notice what happens here: a new contributor can read the five declaration files and understand the entire shape of the type system without ever opening a single impl file. The architecture is not buried inside method bodies -- it is the first thing you see. This is a powerful property for any codebase, and it becomes increasingly valuable as systems grow in complexity.
Readable by humans and AI models alike#

Declaration files are naturally high signal, low noise. They contain type signatures, docstrings, field definitions, and method groupings -- precisely the information needed to understand a module's role. This property benefits two distinct audiences:

    Human readers skimming a codebase: declaration files function as self-maintaining documentation. Unlike comments or external docs that can drift out of sync, the declarations are the interface -- they are always accurate because the compiler enforces them.
    AI models analyzing code: Large language models operate within limited context windows. Feeding a model a 250-line declaration file gives it a complete understanding of a module's capabilities without spending tokens on implementation details. When an AI needs to generate code that interacts with a module, the declaration file provides exactly the right level of abstraction.

This dual benefit is worth keeping in mind as you design your own modules. Ask yourself: "Could someone -- human or machine -- understand what this module does by reading its declaration file alone?" If the answer is yes, you have achieved a good separation.
Granular separation of concerns#

The impl system enables decomposition at a finer grain than files or classes alone can provide. Consider this: a single object with 80 methods does not need to live in one monolithic file. Its implementations can be split by feature domain:

na_ir_gen_pass.jac              # One object, 80+ method signatures
na_ir_gen_pass.impl/
    tuples.impl.jac             # Just the tuple-related methods
    exceptions.impl.jac         # Just the exception-handling methods
    dicts.impl.jac              # Just the dictionary methods
    ...19 files total

(Browse this example on GitHub)

Each impl file becomes a focused, self-contained unit. A developer working on tuple code generation opens tuples.impl.jac and nothing else. They do not need to scroll past 2,000 lines of unrelated code, and their changes will not produce merge conflicts with a colleague working on exception handling in a different file. In a collaborative setting, this kind of isolation is invaluable.
Cleaner folder architecture#

Without separation, large packages tend to devolve into a flat list of large files where understanding the system requires opening each one and reading deeply. With separation, the folder structure itself communicates the architecture:

    Declaration files at the package root answer the question: "What does this package contain?"
    The impl/ directory answers: "Where is the logic?" -- without cluttering the root
    Feature-named impl files answer: "What concerns does this module address?"

The result is a codebase where running ls *.jac in any directory gives you an architectural overview, while the impl/ directory is where you go when you need the details. Think of it like a well-organized textbook: the table of contents (declarations) tells you what topics are covered, while the chapters (implementations) contain the full exposition.
Overview of Patterns#

Now that we understand the motivation, let us survey the five organizational patterns available to you. The table below provides a quick reference; we will examine each pattern in detail in the sections that follow.
Pattern 	File Layout 	When to Use 	Compiler Example
Inline 	Single .jac file, declarations + impl blocks together 	Small modules (<100 lines) 	langserve/rwlock.jac
Side-by-Side 	mod.jac + impl/mod.impl.jac 	Medium modules, clean interface/impl split 	cli/command.jac
Shared impl/ Directory 	Multiple .jac files + one impl/ directory 	Package-level organization 	cli/commands/
.impl/ Directory 	mod.jac + mod.impl/*.impl.jac 	Very large modules, many concerns 	na_ir_gen_pass.jac
Pure Declarations 	.jac file with only type/object definitions 	Data models, re-exports 	estree.jac
Inline (All-in-One)#

The simplest pattern: declarations and implementations live together in a single file. This is the natural starting point for any small, self-contained module where introducing a separate impl file would add overhead without improving clarity.
What it looks like#

obj ReadWriteLock {
    
has _cond: threading.Condition by postinit,
        
_readers: int = 0,
        
_writer: bool = False;

    
def postinit -> None;
    
def acquire_read -> None;
    
def release_read -> None;
    
def acquire_write -> None;
    
def release_write -> None;
}

impl ReadWriteLock.postinit -> None {
    
self._cond = threading.Condition(threading.Lock());
}

impl ReadWriteLock.acquire_read -> None {
    
with self._cond {
        
while self._writer {
            
self._cond.wait();
        
}
        
self._readers += 1;
    
}
}

# ... remaining impls in the same file

Notice how the declaration block at the top still reads like a concise API summary, while the impl blocks below provide the full details. Even within a single file, the logical separation between what and how remains clear.
Real example#

jaclang/langserve/rwlock.jac -- A read-write lock in 94 lines. The declaration block (lines 1-29) reads like an API summary, and the impl blocks follow immediately. At this size, introducing a second file would be unnecessary overhead.
When to use#

    The module totals fewer than ~100 lines
    The type has few methods with short implementations
    The module is self-contained, with no external consumers who would benefit from reading the interface in isolation

Side-by-Side Impl File (1:1)#

As a module grows beyond the inline threshold, the next natural step is to split it into two files: one for declarations and one for implementations. The compiler auto-discovers mod.impl.jac as the annex for mod.jac, or finds impl/mod.impl.jac in a sibling impl/ directory.
What it looks like#

command.jac -- declarations only:

"""CLI command model and argument definitions."""

enum ArgKind {
    
POSITIONAL,
    
OPTIONAL,
    
FLAG,
    
REMAINDER
}

obj Arg {
    
has name: str,
        
kind: ArgKind = ArgKind.OPTIONAL,
        
typ: type = str,
        
default: object = None,
        
help: str = "";

    
static def create(name: str, ...) -> Arg;
}

obj Command {
    
has name: str,
        
func: Callable,
        
args: list[Arg] = [],
        
help: str = "";

    
def execute(parsed_args: dict) -> int;
}

impl/command.impl.jac -- all logic:

impl Arg.create(name: str, ...) -> Arg {
    
# ... construction logic
}

impl Command.execute(parsed_args: dict) -> int {
    
# ... execution logic
}

Observe how the declaration file reads almost like a specification document: you can see every type, every field, and every method signature at a glance. The impl file, meanwhile, contains only the method bodies -- the "how" behind the "what."
Real example#

jaclang/cli/command.jac + jaclang/cli/impl/command.impl.jac -- The declaration file defines the Arg, ArgKind, and Command types that the entire CLI system depends on. The impl file provides the method bodies. Anyone reading command.jac instantly grasps the full API without scrolling through implementation details.
When to use#

    The module has a clear interface that benefits from being readable on its own
    Implementation is substantial (100+ lines of method bodies)
    Other modules import from this one and their authors only need to understand the interface

Shared impl/ Directory (Many:Many)#

When a package contains multiple related modules, each of medium size, a shared impl/ directory provides an elegant and consistent layout. Each declaration file has a corresponding impl/name.impl.jac. This is the dominant pattern throughout the Jac compiler codebase, and for good reason -- it scales naturally as packages grow.
What it looks like#

cli/commands/
├── analysis.jac
├── config.jac
├── execution.jac
├── project.jac
├── tools.jac
├── transform.jac
└── impl/
    ├── analysis.impl.jac
    ├── config.impl.jac
    ├── execution.impl.jac
    ├── project.impl.jac
    ├── tools.impl.jac
    └── transform.impl.jac

Real example#

jaclang/cli/commands/ -- Six command group files, each declaring functions with rich decorator metadata (command names, argument specs, help text, usage examples). The impl/ directory holds the actual command logic.

The declaration file functions as a command catalog -- study this example carefully:

"""Execution commands: run, enter, serve, debug."""

@registry.command(
    
name="run",
    
help="Run a Jac program",
    
args=[
        
Arg.create("filename", kind=ArgKind.POSITIONAL, help="Path to .jac file"),
        
Arg.create("cache", typ=bool, default=True, help="Enable compilation cache"),
    
],
    
examples=[
        
("jac run hello.jac", "Run a simple program"),
    
],
    
group="execution"
)
def run(filename: str, main: bool = True, cache: bool = True) -> int;

The impl file then provides the body:

impl run(filename: str, main: bool = True, cache: bool = True) -> int {
    
_ensure_jac_runtime();
    
_discover_config_from_file(filename);
    
(base, mod, mach) = _proc_file(filename);
    
# ... full implementation
}

Notice how the declaration file alone tells you everything you need to know about what the command does, what arguments it accepts, and how it should be invoked. The impl file is only needed when you want to understand or modify the internal logic.
Where it's used in the compiler#

To appreciate how pervasive this pattern is, here is a sampling from across the compiler codebase:
Package 	Declaration Files 	impl/ Contents
cli/commands/ 	6 command group files 	6 matching impl files
compiler/passes/main/ 	6 compiler pass files 	6 matching impl files
compiler/passes/tool/ 	8 tool pass files 	8 matching impl files
jac0core/passes/ 	8 pass files 	8 matching impl files
jac0core/ 	unitree.jac, program.jac, plugin.jac, etc. 	Matching impl files
langserve/ 	server.jac, engine.jac, utils.jac, etc. 	Matching impl files
runtimelib/ 	context.jac, memory.jac, server.jac, etc. 	Matching impl files
project/ 	config.jac, dependencies.jac, etc. 	Matching impl files
When to use#

    A package contains multiple related modules
    You want a consistent, predictable layout across the entire package
    Each module is medium-sized (not large enough to warrant its own impl directory)

.impl/ Directory (1:Many)#

When a single class grows to contain dozens of methods spanning many distinct concerns, the side-by-side pattern is no longer sufficient. The .impl/ directory pattern addresses this by splitting one declaration file's implementations across multiple feature-focused files.

This is, in a sense, the most powerful pattern -- it allows a single type's implementation to be decomposed along conceptual boundaries rather than being forced into a single monolithic file.
What it looks like#

compiler/passes/native/
├── na_ir_gen_pass.jac                    # All declarations (277 lines)
└── na_ir_gen_pass.impl/
    ├── core.impl.jac                     # init, transform, main pass
    ├── stmt.impl.jac                     # statement codegen
    ├── expr.impl.jac                     # expression codegen
    ├── func.impl.jac                     # function/ability codegen
    ├── calls.impl.jac                    # function call codegen
    ├── objects.impl.jac                  # archetype/class codegen
    ├── vtable.impl.jac                   # virtual dispatch tables
    ├── tuples.impl.jac                   # tuple codegen
    ├── lists.impl.jac                    # list codegen
    ├── dicts.impl.jac                    # dictionary codegen
    ├── sets.impl.jac                     # set codegen
    ├── enums.impl.jac                    # enum codegen
    ├── builtins.impl.jac                 # builtin functions
    ├── globals.impl.jac                  # global variables
    ├── comprehensions.impl.jac           # list/dict/set comprehensions
    ├── exceptions.impl.jac               # try/catch/raise
    ├── file_io.impl.jac                  # file I/O
    ├── context_mgr.impl.jac             # with statements
    └── types.impl.jac                    # type resolution helpers

Real example#

jaclang/compiler/passes/native/na_ir_gen_pass.jac -- The LLVM IR generation pass. Let us examine how the declaration file defines a single NaIRGenPass object with 80+ method signatures, carefully organized by compiler phase:

"""Native LLVM IR generation pass."""

obj NaIRGenPass(Transform) {
    
def init(ir_in: uni.Module, prog: object) -> None;
    
# Main pass logic
    
def transform(ir_in: uni.Module) -> uni.Module;
    
# Body / statement codegen
    
def _codegen_body(stmts: (list | tuple)) -> None;
    
def _codegen_stmt(nd: uni.UniNode) -> None;
    
def _codegen_if(nd: uni.IfStmt) -> None;
    
def _codegen_while(nd: uni.WhileStmt) -> None;
    
# Expression codegen
    
def _codegen_expr(nd: (uni.UniNode | None)) -> (ir.Value | None);
    
def _codegen_binary(nd: uni.BinaryExpr) -> (ir.Value | None);
    
# Phase 9: Tuples
    
def _codegen_tuple_val(nd: uni.TupleVal) -> (ir.Value | None);
    
# ... 80+ more methods across 16 phases
}

Each impl file then handles one domain. Here, for instance, is how the tuple-related methods are isolated:

# tuples.impl.jac
"""Tuple codegen and unpacking."""

impl NaIRGenPass._codegen_tuple_val(nd: uni.TupleVal) -> (ir.Value | None) {
    
# ... tuple codegen logic
}

impl NaIRGenPass._codegen_tuple_unpack(targets: list, ...) -> None {
    
# ... unpacking logic
}

impl NaIRGenPass._get_struct_size(struct_type: ir.LiteralStructType) -> int {
    
# ... size calculation
}

Also worth studying: jaclang/compiler/type_system/type_evaluator.jac + type_evaluator.impl/ (5 files: core evaluation, type construction, utilities, imports, parameter checking).
When to use#

    A single class has dozens of methods spanning many distinct concerns
    The combined implementation would exceed 1,000 lines in a single file
    Different developers may work on different feature areas simultaneously
    The declaration file alone should serve as a complete API reference for the type

Pure Declarations (Data Modules)#

Some modules are primarily -- or entirely -- composed of declarations: type definitions, data classes, enums, constants, or re-exports. These modules need little or no implementation logic, and that is perfectly fine. Recognizing when a module fits this pattern helps you avoid creating unnecessary impl files.
What it looks like#

estree.jac -- 580 lines of ESTree AST node type definitions:

"""ESTree AST Node Definitions for ECMAScript."""

obj SourceLocation {
    
has source: (str | None) = None,
        
start: (Position | None) = None,
        
end: (Position | None) = None;
}

obj Position {
    
has line: int = 0,
        
column: int = 0;
}

obj Identifier(Node) {
    
has name: str = '',
        
`type: TypingLiteral['Identifier'] = 'Identifier';
}

# ... 60+ more node types

Its impl file (impl/estree.impl.jac) is only 33 lines -- a single utility function. The vast majority of the module's value is in the declarations themselves.

constructs.jac -- A 35-line re-export barrel:

"""Core constructs for Jac Language - re-exports."""

import from jaclang.jac0core.archetype {
    
AccessLevel, Anchor, Archetype, Root, ...
}

glob __all__ = ['AccessLevel', 'Anchor', ...];

When to use#

    The module is primarily a data model (types, enums, constants)
    Objects have has fields but few or no methods
    The file serves as a public API barrel that re-exports from internal modules

Choosing a Pattern#

With five patterns at your disposal, how do you decide which one to use? The following decision guide will help you navigate the choice based on your module's characteristics:

Is the module mostly data types with few methods?
  └─ Yes → Pure Declarations
  └─ No ↓

Is the total code (decl + impl) under ~100 lines?
  └─ Yes → Inline
  └─ No ↓

Does one class have 20+ methods spanning multiple concerns?
  └─ Yes → .impl/ Directory (1:Many)
  └─ No ↓

Are there multiple related modules in this package?
  └─ Yes → Shared impl/ Directory
  └─ No → Side-by-Side Impl File (1:1)

Work through this decision tree from top to bottom, and you will arrive at the appropriate pattern for your situation.

No wrong answer

These patterns are conventions, not rigid rules. The compiler codebase uses all five, sometimes in adjacent directories. The goal is always the same: pick the pattern that makes your declaration files most readable as standalone documentation of your module's API. When in doubt, start with the simpler pattern and refactor to a more structured one as the module grows.
Best Practices#

Let us conclude with a set of best practices distilled from the compiler codebase. These guidelines will help you get the most out of Jac's impl system regardless of which pattern you choose.

Declaration files are your API docs

Write declaration files as if they are the first thing a new team member will read. Include docstrings, organize methods by concern, and use comments to create logical groupings among related declarations. A well-written declaration file should make its module's purpose and capabilities immediately apparent.

Name impl files to match declarations

Always name impl files after their declaration file: server.jac → impl/server.impl.jac or server.impl.jac. This naming convention makes the relationship between declaration and implementation immediately obvious, and it allows the compiler to auto-discover impl files without explicit configuration.

Split impl files by feature, not by class

When using a .impl/ directory, organize files by what they do (tuples.impl.jac, exceptions.impl.jac) rather than by which class they belong to. A single class's methods naturally span multiple feature domains, and grouping by feature makes each file a cohesive, focused unit of work.

Be consistent within a package

If one module in a package uses impl/, all modules in that package should too. Mixing patterns within the same directory creates confusion and makes the project harder to navigate. The compiler codebase follows this principle consistently -- for instance, every module in cli/commands/ uses the shared impl/ pattern.

Private helpers go in the impl file

Helper functions (those prefixed with _) that exist solely to support implementations should live in the impl file, not the declaration file. Keep the declaration file focused on the public API -- it should answer the question "What can this module do?" without revealing "How does it do it internally?"

Here is a concrete example from cli/commands/impl/execution.impl.jac:

# Private helpers alongside impls

def _ensure_jac_runtime -> None {
    
# ... helper logic
}

def _proc_file(filename: str) -> tuple {
    
# ... helper logic
}

impl run(filename: str, ...) -> int {
    
_ensure_jac_runtime();
    
(base, mod, mach) = _proc_file(filename);
    
# ...
}

Notice how the private helpers _ensure_jac_runtime and _proc_file live alongside the implementations that use them. They are implementation details -- they belong with the implementation, not in the declaration file where they would clutter the public interface.
Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Testing
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
            CLI Commands
            Configuration
            Code Organization
            Testing
            Debugging
        Python Integration
        Quick Reference

Table of contents

    Test Syntax
        Basic Test
        Test with Setup
    Assertions
        Basic Assert
        Equality
        Comparisons
        Boolean
        Membership
        Type Checking
        None Checking
        Float Comparison
        With Messages
    CLI Commands
        Running Tests
        CLI Options
        Examples
    Test Output
        Success
        Failure
    Testing Patterns
        Testing Objects
        Testing Nodes and Walkers
        Testing Walker Reports
        Testing Graph Structure
        Testing Exceptions
    Project Organization
        Separate Test Files
        Tests in Same File
    Configuration
        jac.toml
    JacTestClient
        Import
        Creating a Client
        Authentication
        Making Requests
        TestResponse
        Full Example
        HMR Testing
    Parameterized Tests
        Import
        Signature
        Usage
        Custom Test IDs
    Best Practices
        1. Descriptive Names
        2. One Focus Per Test
        3. Isolate Tests
        4. Test Edge Cases
        5. Clear Assertions
    Related Resources

    Full Reference
    Developer Workflow

Testing Reference#

Complete reference for writing and running tests in Jac.
Test Syntax#
Basic Test#

test "my feature" {
    
# Test body
    
assert condition;
}

Test with Setup#

obj MyObject {
    
has data: str;

    
def process() -> str {
        
return self.data;
    
}
}

test "object processing" {
    
# Setup
    
my_obj = MyObject(data="test");

    
# Test
    
result = my_obj.process();

    
# Assert
    
assert result == "test";
}

Assertions#
Basic Assert#

test "basic assert" {
    
assert condition;
    
assert condition, "Error message";
}

Equality#

test "equality checks" {
    
assert a == b;           # Equal
    
assert a != b;           # Not equal
    
assert a is b;           # Same object
    
assert a is not b;       # Different objects
}

Comparisons#

test "comparisons" {
    
assert a > b;            # Greater than
    
assert a >= b;           # Greater or equal
    
assert a < b;            # Less than
    
assert a <= b;           # Less or equal
}

Boolean#

test "boolean values" {
    
assert True;
    
assert not False;
    
assert bool(value);
}

Membership#

test "membership" {
    
assert item in collection;
    
assert item not in collection;
    
assert key in dictionary;
}

Type Checking#

test "type checking" {
    
assert isinstance(obj, MyClass);
    
assert type(obj) == MyClass;
}

None Checking#

test "none checking" {
    
assert value is None;
    
assert value is not None;
}

Float Comparison#

test "float comparison" {
    
result = 0.1 + 0.2;
    
assert almostEqual(result, 0.3, 10);
}

With Messages#

test "assertions with messages" {
    
assert result > 0, f"Expected positive, got {result}";
    
assert len(items) == 3, "Should have 3 items";
}

CLI Commands#
Running Tests#

# Run all tests in a file
jac
 test main.jac

# Run tests in a directory
jac
 test -d tests/

# Run specific test
jac
 test main.jac -t my_feature

CLI Options#
Option 	Short 	Description
--test_name 	-t 	Run specific test by name
--filter 	-f 	Filter tests by pattern
--xit 	-x 	Exit on first failure
--maxfail 	-m 	Stop after N failures
--directory 	-d 	Test directory
--verbose 	-v 	Verbose output
Examples#

# Verbose output
jac
 test main.jac -v

# Stop on first failure
jac
 test main.jac -x

# Filter by pattern
jac
 test main.jac -f "user_"

# Max failures
jac
 test -d tests/ -m 3

# Combined
jac
 test main.jac -t calculator_add -v

File naming

Avoid naming .jac files with a test_ prefix (e.g., test_utils.jac), as this can conflict with Python's module import system. Use descriptive names like utils_tests.jac or my_app.jac instead.
Test Output#
Success#

unittest.case.FunctionTestCase (test_add) ... ok
unittest.case.FunctionTestCase (test_subtract) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK

Failure#

unittest.case.FunctionTestCase (test_add) ... FAIL

======================================================================
FAIL: test_add
----------------------------------------------------------------------
AssertionError: Expected 5, got 4

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)

Testing Patterns#
Testing Objects#

obj Calculator {
    
has value: int = 0;

    
def add(n: int) -> int {
        
self.value += n;
        
return self.value;
    
}

    
def reset() -> None {
        
self.value = 0;
    
}
}

test "calculator add" {
    
calc = Calculator();
    
assert calc.add(5) == 5;
    
assert calc.add(3) == 8;
    
assert calc.value == 8;
}

test "calculator reset" {
    
calc = Calculator();
    
calc.add(10);
    
calc.reset();
    
assert calc.value == 0;
}

Testing Nodes and Walkers#

node Counter {
    
has count: int = 0;
}

walker Incrementer {
    
has amount: int = 1;

    
can start with Root entry {
        
visit [-->];
    
}

    
can increment with Counter entry {
        
here.count += self.amount;
    
}
}

test "walker increments" {
    
counter = root ++> Counter();
    
root spawn Incrementer();
    
assert counter[0].count == 1;
}

test "walker custom amount" {
    
counter = root ++> Counter();
    
root spawn Incrementer(amount=5);
    
assert counter[0].count == 5;
}

Testing Walker Reports#

node Person {
    
has name: str;
    
has age: int;
}

walker FindAdults {
    
can check with Root entry {
        
for person in [-->](?:Person) {
            
if person.age >= 18 {
                
report person;
            
}
        
}
    
}
}

test "find adults" {
    
root ++> Person(name="Alice", age=30);
    
root ++> Person(name="Bob", age=15);
    
root ++> Person(name="Carol", age=25);

    
result = root spawn FindAdults();

    
assert len(result.reports) == 2;
    
names = [p.name for p in result.reports];
    
assert "Alice" in names;
    
assert "Carol" in names;
    
assert "Bob" not in names;
}

Testing Graph Structure#

node Room {
    
has name: str;
}

edge Door {}

test "graph connections" {
    
kitchen = Room(name="Kitchen");
    
living = Room(name="Living Room");
    
bedroom = Room(name="Bedroom");

    
root ++> kitchen;
    
kitchen +>: Door() :+> living;
    
living +>: Door() :+> bedroom;

    
# Test connections
    
assert len([root -->]) == 1;
    
assert len([kitchen -->]) == 1;
    
assert len([living -->]) == 1;
    
assert len([bedroom -->]) == 0;

    
# Test connectivity
    
assert living in [kitchen ->:Door:->];
    
assert bedroom in [living ->:Door:->];
}

Testing Exceptions#

def divide(a: int, b: int) -> float {
    
if b == 0 {
        
raise ZeroDivisionError("Cannot divide by zero");
    
}
    
return a / b;
}

test "divide normal" {
    
assert divide(10, 2) == 5;
}

test "divide by zero" {
    
try {
        
divide(10, 0);
        
assert False, "Should have raised error";
    
} except ZeroDivisionError {
        
assert True;  # Expected
    
}
}

test "divide negative" {
    
assert divide(-10, 2) == -5;
}

Project Organization#
Separate Test Files#

myproject/
├── jac.toml
├── src/
│   ├── models.jac
│   └── walkers.jac
└── tests/
    ├── test_models.jac
    └── test_walkers.jac

# Run all tests
jac
 test -d tests/

# Run specific file
jac
 test tests/test_models.jac

Tests in Same File#

# models.jac

obj User {
    
has name: str;
    
has email: str;

    
def is_valid() -> bool {
        
return len(self.name) > 0 and "@" in self.email;
    
}
}

# Tests at bottom
test "user valid" {
    
user = User(name="Alice", email="alice@example.com");
    
assert user.is_valid();
}

test "user invalid email" {
    
user = User(name="Alice", email="invalid");
    
assert not user.is_valid();
}

test "user empty name" {
    
user = User(name="", email="alice@example.com");
    
assert not user.is_valid();
}

Configuration#
jac.toml#

[test]
directory = "tests"
verbose = true
fail_fast = false
max_failures = 10

JacTestClient#

JacTestClient provides an in-process HTTP client for testing Jac API endpoints without starting a real server or opening network ports.
Import#

from jaclang.runtimelib.testing import JacTestClient

Creating a Client#

# Create from a .jac file
client = JacTestClient.from_file("app.jac")

# With a custom base path (useful for temp directories in tests)
client = JacTestClient.from_file("app.jac", base_path="/tmp/test")

Authentication#

# Register a test user
response = client.register_user("testuser", "password123")

# Login
response = client.login("testuser", "password123")

# Manually set auth token
client.set_auth_token("eyJ...")

# Clear auth
client.clear_auth()

Making Requests#

# GET request
response = client.get("/walker/get_users")

# POST request with JSON body
response = client.post("/walker/create_user", json={"name": "Alice"})

# PUT request
response = client.put("/walker/update_user", json={"name": "Bob"})

# Generic request
response = client.request("DELETE", "/walker/delete_user", json={"id": "123"})

# With custom headers
response = client.get("/walker/data", headers={"X-Custom": "value"})

TestResponse#

Responses from JacTestClient are TestResponse objects:
Property/Method 	Type 	Description
status_code 	int 	HTTP status code
headers 	dict 	Response headers
text 	str 	Raw response body
json() 	dict 	Parse body as JSON
ok 	bool 	True if status is 2xx
data 	dict \| None 	Unwrapped data from TransportResponse envelope
Full Example#

import pytest
from jaclang.runtimelib.testing import JacTestClient

def test_task_crud(tmp_path):
    
client = JacTestClient.from_file("app.jac", base_path=str(tmp_path))

    
# Register and authenticate
    
client.register_user("testuser", "password123")

    
# Create
    
resp = client.post("/walker/CreateTask", json={"title": "My Task"})
    
assert resp.status_code == 200
    
assert resp.ok

    
# Read
    
resp = client.post("/walker/GetTasks")
    
data = resp.json()
    
assert len(data["reports"]) == 1

    
# Cleanup
    
client.close()

HMR Testing#

Test hot module replacement behavior:

def test_hmr(tmp_path):
    
client = JacTestClient.from_file("app.jac", base_path=str(tmp_path))
    
client.register_user("user", "pass")

    
# Initial state
    
resp = client.post("/walker/get_data")
    
assert resp.ok

    
# Simulate file change and reload
    
client.reload()

    
# Verify after reload
    
resp = client.post("/walker/get_data")
    
assert resp.ok

    
client.close()

Parameterized Tests#

The parametrize() helper registers one test per parameter, similar to pytest.mark.parametrize. It creates individual test cases from a list of inputs, so each case runs and reports independently.
Import#

import from jaclang.runtimelib.test { parametrize }

Signature#

parametrize(base_name: str, params: Iterable, test_func: Callable, id_fn: Callable | None = None)

Parameter 	Type 	Description
base_name 	str 	Base name for the generated tests
params 	Iterable 	List of parameter values, each passed to the test function
test_func 	Callable 	Test function to invoke with each parameter
id_fn 	Callable \| None 	Optional function to generate test IDs from each parameter
Usage#

Define a test function that takes a single parameter, then call parametrize() in a with entry block:

import from jaclang.runtimelib.test { parametrize }

def _test_square(pair: tuple) {
    
input_val = pair[0];
    
expected = pair[1];
    
result = input_val ** 2;
    
assert result == expected, f"Expected {expected}, got {result}";
}

with entry {
    
parametrize(
        
"square",
        
[(2, 4), (3, 9), (0, 0), (-1, 1)],
        
_test_square
    
);
}

This registers four tests: square_0, square_1, square_2, square_3.
Custom Test IDs#

Use id_fn to generate descriptive test names:

import from jaclang.runtimelib.test { parametrize }

def _test_parse(raw: str) {
    
# test logic
}

with entry {
    
parametrize(
        
"parse values",
        
["500m", "2", "250"],
        
_test_parse,
        
id_fn=lambda p: str -> str { return f"input_{p}"; }
    
);
}

Best Practices#
1. Descriptive Names#

# Good - use readable descriptions
test "user creation with valid email" { }
test "walker visits all connected nodes" { }

# Avoid - vague or cryptic names
test "t1" { }
test "thing" { }

2. One Focus Per Test#

# Good - focused tests
test "add positive numbers" {
    
assert add(2, 3) == 5;
}

test "add negative numbers" {
    
assert add(-2, -3) == -5;
}

# Avoid - too broad
test "all math operations" {
    
assert add(2, 3) == 5;
    
assert subtract(5, 3) == 2;
    
assert multiply(2, 3) == 6;
}

3. Isolate Tests#

# Good - creates fresh state
test "counter increment" {
    
counter = root ++> Counter();
    
root spawn Incrementer();
    
assert counter[0].count == 1;
}

# Each test should be independent
test "counter starts at zero" {
    
counter = Counter();
    
assert counter.count == 0;
}

4. Test Edge Cases#

test "empty list" {
    
result = process([]);
    
assert result == [];
}

test "single item" {
    
result = process([1]);
    
assert len(result) == 1;
}

test "large list" {
    
result = process(list(range(1000)));
    
assert len(result) == 1000;
}

5. Clear Assertions#

# Good - clear what failed
test "calculation with message" {
    
result = calculate(input);
    
assert result == expected, f"Expected {expected}, got {result}";
}

# Avoid - unclear failures
test "calculation no message" {
    
assert calculate(input) == expected;
}

Related Resources#

    CLI Reference

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Debugging
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
            CLI Commands
            Configuration
            Code Organization
            Testing
            Debugging
        Python Integration
        Quick Reference

Table of contents

    Quick Start
    What is the Jac Debugger?
    One-Time Setup
        Requirements
        Enable Breakpoints in VS Code
        Install Jac Extension
    Project Setup
        Create launch.json
    Using Breakpoints
        Setting a Breakpoint
        Running the Debugger
        Debugger Controls
        Inspecting Variables
    Graph Visualization
        Example Graph Program
        Opening the Graph Visualizer
        Watching the Graph Build
    Troubleshooting
    Next Steps

    Full Reference
    Developer Workflow

Debugging in VS Code#

Debug your Jac programs with breakpoints, variable inspection, and graph visualization.

    Prerequisites

        Python 3.12+
        jaclang installed
        VS Code with Jac extension
        Time: ~15 minutes

Quick Start#

If you're already familiar with debuggers:

    Install Python 3.12+ and jaclang
    Install VS Code + Jac extension
    Create launch.json (Debug and Run > Create launch.json > Jac Debug)
    Open VS Code Command Palette and run jacvis for graph visualization
    Set a breakpoint > Run Debugger > Inspect variables

What is the Jac Debugger?#

The Jac Debugger helps you find and fix issues in Jac programs. It supports:

    Breakpoints - Pause execution at specific lines
    Step-through execution - Execute code line by line
    Variable inspection - View local and global variable values
    Graph visualization - Unique to Jac: see your nodes and edges visually

One-Time Setup#

Complete these steps once per computer.
Requirements#
Requirement 	How to Check
Python 3.12+ 	python --version
jaclang 	jac --version
VS Code 	Download
Jac Extension 	Extensions tab > search "Jac"
Enable Breakpoints in VS Code#

To set breakpoints in Jac files:

    Open VS Code Settings
    Search for "breakpoints"
    Enable Debug: Allow Breakpoints Everywhere

Install Jac Extension#

    Open VS Code Extensions panel
    Search for "Jac"
    Click Install

Project Setup#

Do this for each new Jac project.
Create launch.json#

launch.json tells VS Code how to run the debugger.

    Open the Run and Debug panel (Ctrl+Shift+D / Cmd+Shift+D)
    Click Create a launch.json file
    Select Jac Debug
    VS Code generates the configuration automatically

Your .vscode/launch.json will look like:

{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "jac",
            "request": "launch",
            "name": "Jac Debug",
            "program": "${file}"
        }
    ]
}

Using Breakpoints#

Breakpoints pause execution so you can inspect program state.
Setting a Breakpoint#

Click in the gutter (left of the line number) to set a breakpoint:

def complex_calculation(x: int, y: int) -> int {
    
result = x * 2;          # <- Set breakpoint here
    
result = result + y;
    
result = result ** 2;
    
return result;
}

with entry {
    
answer = complex_calculation(5, 3);
    
print(answer);
}

Running the Debugger#

    Set your breakpoint
    Press F5 or click Run and Debug
    The program pauses at the breakpoint

Debugger Controls#
Action 	Shortcut 	Description
Continue 	F5 	Run until next breakpoint
Step Over 	F10 	Execute line, skip into functions
Step Into 	F11 	Execute line, enter functions
Step Out 	Shift+F11 	Run until current function returns
Restart 	Ctrl+Shift+F5 	Restart from beginning
Stop 	Shift+F5 	Stop debugging
Inspecting Variables#

When paused, the Variables panel shows:

    Local Variables - Variables in the current function scope
    Global Variables - Variables defined at module level

Graph Visualization#

Jac's debugger includes a visual tool to see your graph structure in real time.
Example Graph Program#

node Person {
    
has age: int;
}

with entry {
    
# Create people nodes
    
jonah = Person(16);
    
sally = Person(17);
    
teacher = Person(42);
    
jonah_mom = Person(45);

    
# Connect Jonah to root
    
root ++> jonah;

    
# Create Jonah's relationships
    
jonah ++> jonah_mom;
    
jonah ++> teacher;
    
jonah ++> sally;
}

Opening the Graph Visualizer#

    Open the VS Code Command Palette:
        Windows/Linux: Ctrl+Shift+P
        macOS: Cmd+Shift+P
    Type jacvis
    Select jacvis: Visualize Jaclang Graph

A side panel opens showing your graph.
Watching the Graph Build#

    Open the graph visualizer panel
    Set a breakpoint in your code
    Start debugging (F5)
    Step through the code - watch nodes and edges appear in real time

You can drag nodes around to better visualize the structure.
Troubleshooting#
Problem 	Solution
Breakpoints are grey / don't trigger 	Enable Debug: Allow Breakpoints Everywhere in VS Code settings
"No Jac debugger found" 	Reload VS Code window after installing Jac extension
Program runs but debugger doesn't stop 	Use Run and Debug (F5), not the terminal
Graph doesn't update 	Open jacvis before starting the debugger
Next Steps#

    Testing Your Code - Write and run tests
    Object-Spatial Programming - Learn about nodes, edges, and walkers

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Interoperability
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
            Interoperability
            Library Mode
        Quick Reference

Table of contents

    Jac Supersets Python
        How it Works: Transpilation to Native Python
        Seamless Interoperability: Import Jac Files Like Python Modules
        Five Adoption Patterns: Choose Your Integration Level
            Pattern Comparison Table
        Pattern Details and Examples
            Pattern 1: Pure Jac
            Pattern 2: Jac + Inline Python
            Pattern 3: Mostly Jac
            Pattern 4: Mostly Python
            Pattern 5: Pure Python + Jac Library
        Key Takeaways
        Using Jac from Python
    Type Compatibility

    Full Reference
    Python Integration

Python Integration#

    Related: Library Mode | Build an AI Day Planner

Jac Supersets Python#

Jac supersets Python and JavaScript, providing full compatibility with both the PyPI and npm ecosystems. Developers can leverage their existing knowledge while accessing new capabilities for graph-based and object-spatial programming.
How it Works: Transpilation to Native Python#

Jac programs execute on the standard Python runtime without requiring custom runtime environments, virtual machines, or interpreters. The Jac compiler transpiles Jac source code into standard Python through a multi-stage compilation pipeline that generates optimized Python bytecode. This approach provides several advantages:

    Standard Python Runtime: Jac programs execute on the Python runtime, utilizing Python's garbage collector, memory management, and threading model.
    Full Ecosystem Access: All packages on PyPI, internal libraries, and Python development tools are compatible with Jac.
    Readable Output: The transpiled Python code is clean and maintainable, enabling inspection, debugging, and understanding.

The relationship between Jac and Python is analogous to that of TypeScript and JavaScript: a superset language that compiles to a widely-adopted base language.

Example: From Jac to Python

The following Jac module demonstrates functions, objects, and an entrypoint:

"""Functions in Jac."""

def factorial(n: int) -> int {
    
if n == 0 { return 1; }
    
else { return n * factorial(n-1); }
}

obj Person {
    
has name: str;
    
has age: int;

    
def greet() -> None {
        
print(f"Hello, my name is {self.name} and I'm {self.age} years old.");
    
}
}

with entry {
    
person = Person("John", 42);
    
person.greet();
    
print(f"5! = {factorial(5)}");
}

The Jac compiler converts this code into the following Python implementation:

"""Functions in Jac."""
from __future__ import annotations
from jaclang.lib import Obj

def factorial(n: int) -> int:
    
if n == 0:
        
return 1
    
else:
        
return n * factorial(n - 1)

class Person(Obj):
    
name: str
    
age: int

    
def greet(self) -> None:
        
print(f"Hello, my name is {self.name} and I'm {self.age} years old.")

person = Person('John', 42)
person.greet()
print(f'5! = {factorial(5)}')

The compiled output demonstrates how Jac's object-oriented features map to standard Python classes inheriting from Obj (Jac's base object archetype), with imports from the jaclang.lib package.
Seamless Interoperability: Import Jac Files Like Python Modules#

Jac integrates with Python through a simple import mechanism. By adding import jaclang to Python code, developers can import .jac files using standard Python import statements without requiring build steps, compilation commands, or configuration files.

Key Integration Features:

    Bidirectional Module Imports: Python files can import Jac modules, and Jac files can import Python modules using standard import syntax. Modules written in .jac and .py can be used interchangeably within a project.

    Incremental Adoption: Jac can be added to existing Python projects without restructuring the codebase. Python files can remain unchanged while Jac modules are introduced where beneficial.

    Standard Import Syntax: The same import statements used for Python modules work with .jac files, requiring no special syntax or additional tools.

Example: Importing Across Languages

Consider a Jac module containing graph utilities:

# graph_tools.jac
node Task {
    
has name: str;
    
has priority: int;
}

This module can be imported in Python using standard import syntax:

# main.py
import jaclang  # Enable Jac imports (one-time setup)
from graph_tools import Task  # Import from .jac file

# Use Jac classes in Python
my_task = Task(name="Deploy", priority=1)

Jac files can also import Python libraries:

# analyzer.jac
import pandas as pd;
import numpy as np;
import from sklearn.linear_model { LinearRegression }

with entry {
    
# NumPy
    
arr = np.array([1, 2, 3, 4, 5]);
    
print(f"Mean: {np.mean(arr)}");

    
# Pandas
    
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]});
    
print(df.describe());

    
# Scikit-learn
    
model = LinearRegression();
}

Inline Python with ::py:: Blocks

For performance-critical code or complex Python-only APIs, embed Python directly in .jac files:

::py::
import numpy as np

def complex_calculation(data):
    """Pure Python for performance-critical code."""
    
arr = np.array(data)
    
return arr.mean(), arr.std()
::py::

with entry {
    
(mean, std) = complex_calculation([1, 2, 3, 4, 5]);
    
print(f"Mean: {mean}, Std: {std}");
}

When to use inline Python:

    Complex Python-only APIs
    Performance-critical numerical code
    Legacy code integration

When NOT to use inline Python:

    Simple imports (use import instead)
    New code that could use Jac features

Implementation Details: Jac extends Python's native import mechanism using the PEP 302 import hook system. When import jaclang is executed, it registers a custom importer that enables Python to locate and load .jac files. Subsequently, Python's import mechanism automatically checks for .jac files alongside .py files, compiles them transparently, and loads them into the program. This integration makes Jac modules function as first-class citizens within the Python environment.
Five Adoption Patterns: Choose Your Integration Level#

Jac provides five adoption strategies that accommodate different development requirements, ranging from pure Python implementations with Jac library support to fully Jac-based applications. The following patterns represent the primary integration approaches:
Pattern Comparison Table#
Pattern 	Use Case 	Jac Content 	Python Content 	Key Benefits 	Example Scenario
1. Pure Jac 	New projects, microservices 	100% 	0% 	Full Jac language features, modern syntax 	Building a new graph-based application with only .jac files
2. Jac + Inline Python 	Inline Python in Jac files 	Mixed (:🇵🇾: blocks) 	Embedded inline 	Gradual migration, use Python syntax when needed 	.jac files with embedded Python for legacy logic or complex imports
3. Mostly Jac 	Import Python modules into Jac 	80-95% .jac 	5-20% .py 	Jac architecture with existing Python utilities 	Project with .jac files importing your existing .py utility modules
4. Mostly Python 	Import Jac modules into Python 	5-20% .jac 	80-95% .py 	Python codebase with select Jac features 	Python project with .py files importing specialized .jac modules for graphs/AI
5. Pure Python + Jac Library 	Conservative adoption 	0% 	100% 	No new syntax, just Jac runtime capabilities 	Pure .py project using Jac runtime via imports and decorators

Pure Jac
100% .jac files

Jac + Inline Python
::py:: blocks

Mostly Jac
import .py files

Mostly Python
import .jac files

Pure Python
+ Jac Library
Pattern Details and Examples#

Example Project: The following examples demonstrate a task manager application that stores tasks and generates AI-powered task descriptions.

Core Features:

    Task storage with graph-based relationships
    Task validation (title length check)
    AI-generated task descriptions

Each pattern demonstrates a different approach to implementing this application.
Pattern 1: Pure Jac#

This pattern uses exclusively .jac files with no Python files required.

Use Case: New projects requiring full access to Jac language features

Directory Structure:

project/
├── main.jac
├── models.jac
└── utils.jac

main.jac
models.jac
utils.jac

"""Main application."""
import models, utils;

walker TaskCreator {
    
has title: str;

    
can create with Root entry {
        
if utils.validate_title(self.title) {
            
task = models.Task(title=self.title);
            
here ++> task;
            
desc = utils.generate_desc(self.title);
            
print(f" Created: {task.title}");
            
print(f"  AI: {desc}");
        
} else {
            
print(" Title too short!");
        
}
    
}
}

with entry {
    
root spawn TaskCreator(title="Build API");
}

Pattern 2: Jac + Inline Python#

This pattern embeds Python code directly within .jac files using ::py:: blocks, enabling the use of Python-specific libraries or preservation of existing Python code.

Use Case: Incremental migration of Python codebases while maintaining legacy utilities

Directory Structure:

project/
├── main.jac
└── models.jac

main.jac
models.jac

"""Application with inline Python validation."""
import models;

def generate_desc(title: str) -> str {
    
return f"Task description for: {title}";
}

::py::
# Legacy Python validation - kept as-is
def validate_title(title):
    """Complex validation logic from old codebase."""
    
return len(title) > 3 and title.strip() != ""

def get_sample_task():
    """Helper from legacy code."""
    
return {"title": "Build API"}
::py::

walker TaskCreator {
    
can create with Root entry {
        
# Use inline Python functions
        
task_data = get_sample_task();

        
if validate_title(task_data["title"]) {
            
task = models.Task(title=task_data["title"]);
            
here ++> task;
            
desc = generate_desc(task.title);
            
print(f" Created: {task.title}");
            
print(f"  AI: {desc}");
        
} else {
            
print(" Title invalid!");
        
}
    
}
}

with entry {
    
root spawn TaskCreator();
}

This approach preserves tested Python code while introducing Jac features, supporting incremental migration strategies.
Pattern 3: Mostly Jac#

This pattern implements the primary application logic in Jac while importing Python utilities from separate .py files.

Use Case: Jac-first development that leverages existing Python utilities or shared modules

Directory Structure:

project/
├── main.jac
├── models.jac
└── validators.py

main.jac
models.jac
validators.py

"""Main application - imports Python module."""
import models;
import validators;

def generate_desc(title: str) -> str {
    
return f"Task description for: {title}";
}

walker TaskCreator {
    
has title: str;

    
can create with Root entry {
        
# Call Python module functions
        
if validators.validate_title(self.title) {
            
task = models.Task(title=self.title);
            
here ++> task;
            
desc = generate_desc(task.title);
            
print(f" Created: {task.title}");
            
print(f"  AI: {desc}");
        
} else {
            
print(" Title too short!");
        
}
    
}
}

with entry {
    
root spawn TaskCreator(title="Build API");
}

Jac imports Python modules using standard import mechanisms without requiring configuration.
Pattern 4: Mostly Python#

This pattern maintains a Python-first application structure while importing .jac modules for graph-based and AI features.

Use Case: Existing Python projects incorporating Jac's graph-native and AI capabilities

Directory Structure:

project/
├── main.py
├── validators.py
└── task_graph.jac

main.py
validators.py
task_graph.jac

"""Python application importing Jac modules."""
import jaclang  # Enable Jac imports

from validators import validate_title
from task_graph import Task, TaskCreator, generate_desc
from jaclang.lib import spawn, root

def create_task(title: str):
    """Python function using Jac features."""
    
if not validate_title(title):
        
print(" Title too short!")
        
return

    
# Use Jac walker
    
creator = TaskCreator(title=title)
    
spawn(creator, root())

    
# Use Jac's AI
    
desc = generate_desc(title)
    
print(f"  AI: {desc}")

if __name__ == "__main__":
    
create_task("Build API")

This approach maintains familiar Python syntax while providing access to Jac's graph-based and AI features.
Pattern 5: Pure Python + Jac Library#

This pattern uses pure Python with Jac's runtime as a library, without any .jac files.

Use Case: Conservative adoption paths, teams preferring Python syntax, or existing Python projects

Directory Structure:

project/
├── main.py
└── validators.py

main.py
validators.py

"""Pure Python using Jac runtime."""
from jaclang.lib import Node, Walker, on_entry, connect, spawn, root
from validators import validate_title

# Define Task node using Jac base class
class Task(Node):
    
title: str
    
done: bool

    
def __init__(self, title: str):
        
super().__init__()
        
self.title = title
        
self.done = False

# Define walker using Jac decorators
class TaskCreator(Walker):
    
def __init__(self, title: str):
        
super().__init__()
        
self.title = title

    
@on_entry
    
def create(self, here) -> None:
        """Entry point - creates task."""
        
if validate_title(self.title):
            
task = Task(title=self.title)
            
connect(here, task)
            
print(f" Created: {task.title}")
            
# Note: AI features require .jac syntax
        
else:
            
print(" Title too short!")

if __name__ == "__main__":
    
creator = TaskCreator(title="Build API")
    
spawn(creator, root())

This pattern provides graph-based capabilities in pure Python without introducing new syntax, utilizing Jac's object-spatial model through library imports.
Key Takeaways#

Jac's design as a Python superset enables complementary use of both languages rather than requiring a choice between them. Key characteristics include:

    Incremental Adoption: Projects can begin with Pattern 5 (pure Python + Jac library) and progressively adopt Pattern 1 (pure Jac) as requirements evolve
    Full Ecosystem Access: All Python libraries, frameworks, and development tools remain compatible without modification
    Flexible Integration: Five adoption patterns accommodate different team preferences and project requirements
    No Vendor Lock-in: Transpiled Python code is readable and maintainable, providing migration paths if needed
    Transparent Interoperability: PEP 302 import hooks enable seamless bidirectional imports between .jac and .py files

Adoption Pattern 	Learning Curve 	Migration Effort 	Feature Access 	Risk Level
Pattern 1: Pure Jac 	Higher 	Higher 	100% Jac features 	Low
Pattern 2: Jac + Inline Python 	Medium 	Low 	100% Jac features 	Low
Pattern 3: Mostly Jac 	Medium-High 	Medium 	100% Jac features 	Low
Pattern 4: Mostly Python 	Low-Medium 	Low 	Select Jac features 	Low
Pattern 5: Pure Python + Library 	Low 	Very Low 	Core runtime only 	Very Low

Jac accommodates both new application development and enhancement of existing Python codebases, providing structured approaches to graph-based and object-spatial programming while maintaining full Python ecosystem compatibility.
Using Jac from Python#

import jaclang  # Registers the Jac import hook

# Import Jac modules using standard Python import syntax
from my_module import my_function, MyClass

# Use exported functions/classes
result = my_function(arg1, arg2)
instance = MyClass()

Type Compatibility#
Jac Type 	Python Type
int 	int
float 	float
str 	str
bool 	bool
list 	list
dict 	dict
tuple 	tuple
set 	set
None 	None
Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Library Mode
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
            Interoperability
            Library Mode
        Quick Reference

Table of contents

    Introduction
        Converting Jac Code to Pure Python
    The Friends Network Example
        The Jac Code
        The Library Mode Python Equivalent
    Key Concepts Explained
        1. Nodes and Edges
        2. Walkers
        3. Abilities (Event Handlers)
        4. Connecting Nodes
        5. Spawning Walkers
        6. Visiting Nodes
    Complete Library Interface Reference
        Type Aliases & Constants
        Base Classes
        Decorators
        Graph Construction
        Graph Traversal & Walker Operations
        Path Building (Methods on OPath class)
        Node & Edge Operations
        Data Access & Persistence
        Access Control & Permissions
        Module Management & Archetypes
        Testing & Debugging
        LLM & AI Integration
        Runtime & Threading
    Best Practices
        1. Type Hints
        2. Walker State
        3. Path Filtering
        4. Clean Imports
    Migration Guide
        From Jac to Library Mode
    Summary

    Full Reference
    Python Integration

Jac Library Mode#

    Part of: Part IX: Deployment

    Related: Python Integration | Part III: OSP

Introduction#

Jac provides a library mode that enables developers to express all Jac language features as standard Python code. This mode provides complete access to Jac's object-spatial programming capabilities through the jaclang.lib package, allowing developers to work entirely within Python syntax.

Library mode is designed for:

    Python-first teams wanting to adopt Jac's graph-native and AI capabilities without learning new syntax
    Existing Python codebases that need object-spatial architectures and AI integration with zero migration friction
    Understanding Jac's architecture by exploring how its transpilation to Python works under the hood
    Enterprise and corporate environments where introducing standard Python libraries is more acceptable than adopting new language syntax

Converting Jac Code to Pure Python#

The jac jac2py command transpiles Jac source files into equivalent Python code. The generated output:

    Provides clean, ergonomic imports from jaclang.lib with full IDE autocomplete support
    Generates idiomatic Python code with proper type hints and docstrings
    Ensures full compatibility with Python tooling, linters, formatters, and static analyzers

The Friends Network Example#

This section demonstrates Jac's object-spatial programming model through a complete example implementation in library mode.
The Jac Code#

The following example implements a social network graph with person nodes connected by friendship and family relationship edges:

node Person {
    
has name: str;

    
can announce with FriendFinder entry {
        
print(f"{visitor} is checking me out");
    
}
}

edge Friend {}
edge Family {
    
can announce with FriendFinder entry {
        
print(f"{visitor} is traveling to family member");
    
}
}

with entry {
    
# Build the graph
    
p1 = Person(name="John");
    
p2 = Person(name="Susan");
    
p3 = Person(name="Mike");
    
p4 = Person(name="Alice");
    
root ++> p1;
    
p1 +>: Friend :+> p2;
    
p2 +>: Family :+> [p1, p3];
    
p2 +>: Friend :+> p3;
}

walker FriendFinder {
    
has started: bool = False;

    
can report_friend with Person entry {
        
if self.started {
            
print(f"{here.name} is a friend of friend, or family");
        
} else {
            
self.started = True;
            
visit [-->];
        
}
        
visit [edge ->:Family :->];
    
}

    
can move_to_person with Root entry {
        
visit [-->];
    
}
}

with entry {
    
result = FriendFinder() spawn root;
    
print(result);
}

The Library Mode Python Equivalent#

Run jac jac2py friends.jac to generate:
Generated Python code

Key Concepts Explained#
1. Nodes and Edges#

In Jac:

node Person {
    
has name: str;
}

edge Friend {}

In Library Mode:

from jaclang.lib import Node, Edge


class Person(Node):
    
name: str


class Friend(Edge):
    
pass

Graph nodes are implemented by inheriting from the Node base class, while relationships between nodes inherit from the Edge base class. Data fields are defined using standard Python class attributes with type annotations.
2. Walkers#

In Jac:

walker FriendFinder {
    
has started: bool = False;
}

In Library Mode:

from jaclang.lib import Walker


class FriendFinder(Walker):
    
started: bool = False

Walkers are graph traversal agents implemented by inheriting from the Walker base class. Walkers navigate through the graph structure and execute logic at each visited node or edge.
3. Abilities (Event Handlers)#

In Jac:

can report_friend with Person entry {
    
print(f"{here.name} is a friend");
}

In Library Mode:

from jaclang.lib import on_entry


@on_entry
def report_friend(self, here: Person) -> None:
    
print(f"{here.name} is a friend")

Abilities define event handlers that execute when a walker interacts with nodes or edges. The @on_entry decorator marks methods that execute when a walker enters a node or edge, while @on_exit marks exit handlers. The here parameter represents the current node or edge being visited, and the visitor parameter (in node/edge abilities) represents the traversing walker.
4. Connecting Nodes#

In Jac:

node Person {
    
has name: str;
}

edge Friend {}
edge Family {}

with entry {
    
p1 = Person(name="John");
    
p2 = Person(name="Susan");
    
p3 = Person(name="Mike");
    
root ++> p1;                      # Connect root to p1
    
p1 +>: Friend :+> p2;             # Connect p1 to p2 with Friend edge
    
p2 +>: Family :+> [p1, p3];       # Connect p2 to multiple nodes
}

In Library Mode:

from jaclang.lib import connect, root

connect(left=root(), right=p1)
connect(left=p1, right=p2, edge=Friend)
connect(left=p2, right=[p1, p3], edge=Family)

The connect() function creates directed edges between nodes. The edge parameter specifies the edge type class, defaulting to a generic edge if omitted. The function supports connecting a single source node to either a single target node or a list of target nodes.
5. Spawning Walkers#

In Jac:

walker FriendFinder {
    
can find with Root entry {
        
visit [-->];
    
}
}

with entry {
    
result = FriendFinder() spawn root;
}

In Library Mode:

from jaclang.lib import spawn, root

result = spawn(FriendFinder(), root())

The spawn() function initiates a walker at a specified node and begins traversal. The root() function returns the root node of the current graph. The spawn() function returns the walker instance after traversal completion.
6. Visiting Nodes#

In Jac:

edge Family {}

walker Visitor {
    
can traverse with Root entry {
        
visit [-->];                      # Visit all outgoing edges
        
visit [->:Family:->];             # Visit only Family edges
    
}
}

In Library Mode:

from jaclang.lib import visit, refs, OPath

visit(self, refs(OPath(here).edge_out().visit()))
visit(
    
self, refs(OPath(here).edge_out(edge=lambda i: isinstance(i, Family)).edge().visit())
)

The OPath() class constructs traversal paths from a given node. The edge_out() method specifies outgoing edges to follow, while edge_in() specifies incoming edges. The edge() method filters the path to include only edges, excluding destination nodes. The visit() method marks the constructed path for the walker to traverse, and refs() converts the path into concrete node or edge references.
Complete Library Interface Reference#

API Scope Notice

The following reference includes both public API functions available via from jaclang.lib import ... and internal runtime functions that may not be directly importable. Core functions available for import include: connect, disconnect, spawn, root, node, edge, walker, obj, Anchor, NodeAnchor, EdgeAnchor, WalkerAnchor, Root. Other functions listed below may be internal to the runtime and subject to change.
Type Aliases & Constants#
Name 	Type 	Description
TYPE_CHECKING 	bool 	Python typing constant for type checking blocks
EdgeDir 	Enum 	Edge direction enum (IN, OUT, ANY)
DSFunc 	Type 	Data spatial function type alias
Base Classes#
Class 	Description 	Usage
Obj 	Base class for all archetypes 	Generic archetype base
Node 	Graph node archetype 	class MyNode(Node):
Edge 	Graph edge archetype 	class MyEdge(Edge):
Walker 	Graph traversal agent 	class MyWalker(Walker):
Root 	Root node type 	Entry point for graphs
GenericEdge 	Generic edge when no type specified 	Default edge type
OPath 	Object-spatial path builder 	OPath(node).edge_out()
Decorators#
Decorator 	Description 	Usage
@on_entry 	Entry ability decorator 	Executes when walker enters node/edge
@on_exit 	Exit ability decorator 	Executes when walker exits node/edge
@sem(doc, fields) 	Semantic string decorator 	AI/LLM integration metadata
Graph Construction#
Function 	Description 	Parameters
connect(left, right, edge, undir, conn_assign, edges_only) 	Connect nodes with edge 	left: source node(s)
right: target node(s)
edge: edge class (optional)
undir: undirected flag
conn_assign: attribute assignments
edges_only: return edges instead of nodes
disconnect(left, right, dir, filter) 	Remove edges between nodes 	left: source node(s)
right: target node(s)
dir: edge direction
filter: edge filter function
build_edge(is_undirected, conn_type, conn_assign) 	Create edge builder function 	is_undirected: bidirectional flag
conn_type: edge class
conn_assign: initial attributes
assign_all(target, attr_val) 	Assign attributes to list of objects 	target: list of objects
attr_val: tuple of (attrs, values)
Graph Traversal & Walker Operations#
Function 	Description 	Parameters
spawn(walker, node) 	Start walker at node 	walker: Walker instance
node: Starting node
spawn_call(walker, node) 	Internal spawn execution (sync) 	walker: Walker anchor
node: Node/edge anchor
async_spawn_call(walker, node) 	Internal spawn execution (async) 	Same as spawn_call (async version)
visit(walker, nodes) 	Visit specified nodes 	walker: Walker instance
nodes: Node/edge references
disengage(walker) 	Stop walker traversal 	walker: Walker to stop
refs(path) 	Convert path to node/edge references 	path: ObjectSpatialPath
arefs(path) 	Async path references (placeholder) 	path: ObjectSpatialPath
filter_on(items, func) 	Filter archetype list by predicate 	items: list of archetypes
func: filter function
Path Building (Methods on OPath class)#
Method 	Description 	Returns
OPath(node) 	Create path from node 	ObjectSpatialPath
.edge_out(edge, node) 	Filter outgoing edges 	Self (chainable)
.edge_in(edge, node) 	Filter incoming edges 	Self (chainable)
.edge_any(edge, node) 	Filter any direction 	Self (chainable)
.edge() 	Edges only (no nodes) 	Self (chainable)
.visit() 	Mark for visit traversal 	Self (chainable)
Node & Edge Operations#
Function 	Description 	Parameters
get_edges(origin, destination) 	Get edges connected to nodes 	origin: list of nodes
destination: ObjectSpatialDestination
get_edges_with_node(origin, destination, from_visit) 	Get edges and connected nodes 	origin: list of nodes
destination: destination spec
from_visit: include nodes flag
edges_to_nodes(origin, destination) 	Get nodes connected via edges 	origin: list of nodes
destination: destination spec
remove_edge(node, edge) 	Remove edge reference from node 	node: NodeAnchor
edge: EdgeAnchor
detach(edge) 	Detach edge from both nodes 	edge: EdgeAnchor
Data Access & Persistence#
Function 	Description 	Returns
root() 	Get current root node 	Root node instance
get_all_root() 	Get all root nodes 	List of roots
get_object(id) 	Get archetype by ID string 	Archetype or None
object_ref(obj) 	Get hex ID string of archetype 	String
save(obj) 	Persist archetype to database 	None
destroy(objs) 	Delete archetype(s) from memory 	None
commit(anchor) 	Commit data to datasource 	None
reset_graph(root) 	Purge graph from memory 	Count of deleted items
Access Control & Permissions#
Function 	Description 	Parameters
perm_grant(archetype, level) 	Grant public access to archetype 	archetype: Target archetype
level: AccessLevel (READ/CONNECT/WRITE)
perm_revoke(archetype) 	Revoke public access 	archetype: Target archetype
allow_root(archetype, root_id, level) 	Allow specific root access 	archetype: Target
root_id: Root UUID
level: Access level
disallow_root(archetype, root_id, level) 	Disallow specific root access 	Same as allow_root
check_read_access(anchor) 	Check read permission 	anchor: Target anchor
check_write_access(anchor) 	Check write permission 	anchor: Target anchor
check_connect_access(anchor) 	Check connect permission 	anchor: Target anchor
check_access_level(anchor, no_custom) 	Get access level for anchor 	anchor: Target
no_custom: skip custom check
Module Management & Archetypes#
Function 	Description 	Parameters
jac_import(target, base_path, ...) 	Import Jac/Python module 	target: Module name
base_path: Search path
absorb, mdl_alias, override_name, items, reload_module, lng: import options
load_module(module_name, module, force) 	Load module into machine 	module_name: Name
module: Module object
force: reload flag
attach_program(program) 	Attach JacProgram to runtime 	program: JacProgram instance
list_modules() 	List all loaded modules 	Returns list of names
list_nodes(module_name) 	List nodes in module 	module_name: Module to inspect
list_walkers(module_name) 	List walkers in module 	module_name: Module to inspect
list_edges(module_name) 	List edges in module 	module_name: Module to inspect
get_archetype(module_name, archetype_name) 	Get archetype class from module 	module_name: Module
archetype_name: Class name
make_archetype(cls) 	Convert class to archetype 	cls: Class to convert
spawn_node(node_name, attributes, module_name) 	Create node instance by name 	node_name: Node class name
attributes: Init dict
module_name: Source module
spawn_walker(walker_name, attributes, module_name) 	Create walker instance by name 	walker_name: Walker class
attributes: Init dict
module_name: Source module
update_walker(module_name, items) 	Reload walker from module 	module_name: Module
items: Items to update
create_archetype_from_source(source_code, ...) 	Create archetype from Jac source 	source_code: Jac code string
module_name, base_path, cachable, keep_temporary_files: options
Testing & Debugging#
Function 	Description 	Parameters
jac_test(func) 	Mark function as test 	func: Test function
run_test(filepath, ...) 	Run test suite 	filepath: Test file
func_name, filter, xit, maxfail, directory, verbose: test options
report(expr, custom) 	Report value from walker 	expr: Value to report
custom: custom report flag
printgraph(node, depth, traverse, edge_type, bfs, edge_limit, node_limit, file, format) 	Generate graph visualization 	node: Start node
depth: Max depth
traverse: traversal flag
edge_type: filter edges
bfs: breadth-first flag
edge_limit, node_limit: limits
file: output path
format: 'dot' or 'mermaid'
LLM & AI Integration#
Function 	Description 	Use Case
by(model) 	Decorator for LLM-powered functions 	@by(model) def func(): ...
call_llm(model, mtir) 	Direct LLM invocation 	Advanced LLM usage
get_mtir(caller, args, call_params) 	Get method IR for LLM 	LLM internal representation
sem(semstr, inner_semstr) 	Semantic metadata decorator 	@sem("doc", {"field": "desc"})
Runtime & Threading#
Function 	Description 	Parameters
setup() 	Initialize class references 	No parameters
get_context() 	Get current execution context 	Returns ExecutionContext
field(factory, init) 	Define dataclass field 	factory: Default factory
init: Include in init
impl_patch_filename(file_loc) 	Patch function file location 	file_loc: File path for stack traces
thread_run(func, *args) 	Run function in thread 	func: Function
args: Arguments
thread_wait(future) 	Wait for thread completion 	future: Future object
create_cmd() 	Create CLI commands 	No parameters (placeholder)
Best Practices#
1. Type Hints#

Always use type hints for better IDE support:

from typing import Optional


class Person(Node):
    
name: str
    
age: Optional[int] = None

2. Walker State#

Keep walker state minimal and immutable when possible:

class Counter(Walker):
    
count: int = 0  # Simple state

    
@on_entry
    
def increment(self, here: Node) -> None:
        
self.count += 1

3. Path Filtering#

Use lambda functions for flexible filtering:

# Filter by edge type
visit(
    
self,
    
refs(OPath(here).edge_out(edge=lambda e: isinstance(e, (Friend, Family))).visit()),
)

# Filter by node attribute
visit(
    
self,
    
refs(OPath(here).edge_out(node=lambda n: hasattr(n, "active") and n.active).visit()),
)

4. Clean Imports#

Import only what you need:

# Good
from jaclang.lib import Node, Walker, spawn, visit, on_entry

# Avoid
from jaclang.lib import *

Migration Guide#
From Jac to Library Mode#
Jac Syntax 	Library Mode Python
node Person { has name: str; } 	class Person(Node):
    name: str
edge Friend {} 	class Friend(Edge):
    pass
walker W { has x: int; } 	class W(Walker):
    x: int
root ++> node 	connect(root(), node)
a +>: Edge :+> b 	connect(a, b, Edge)
W() spawn root 	spawn(W(), root())
visit [-->] 	visit(self, refs(OPath(here).edge_out().visit()))
visit [<--] 	visit(self, refs(OPath(here).edge_in().visit()))
visit [--] 	visit(self, refs(OPath(here).edge_any().visit()))
can f with T entry {} 	@on_entry
def f(self, here: T): ...
disengage; 	disengage(self)
Summary#

Library mode provides a pure Python implementation of Jac's object-spatial programming model through the jaclang.lib package. This approach offers several advantages:

    Complete Feature Parity: All Jac language features are accessible through the library interface
    Idiomatic Python: Implementation uses standard Python classes, decorators, and functions without runtime magic
    Full Tooling Support: Generated code includes proper type hints, enabling IDE autocomplete, static analysis, and debugging
    Seamless Integration: The library can be incorporated into existing Python projects without requiring build system modifications
    Maintainable Output: Transpiled code is readable and follows Python best practices

Library mode enables developers to leverage Jac's graph-native and AI-integrated programming model while maintaining full compatibility with the Python ecosystem and development workflow.
Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Walker Patterns
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference
            Walker Patterns
            Appendices

Table of contents

    The .reports Array
    Common Patterns
        Pattern 1: Single Report (Recommended)
        Pattern 2: Report Per Node
        Pattern 3: Operation + Result
        Pattern 4: Nested Walker Spawning
        Pattern 5: Multiple Reports (Complex Operations)
    Safe Access Patterns
    Response Object Structure
    Best Practices
    Anti-Patterns
        Don't: Report in a loop without accumulation
        Don't: Assume report order without documentation

    Full Reference
    Quick Reference

Walker Response Patterns#

This reference explains how walker responses work and the common patterns for handling them.

    Related:

        Graph Operations - Node creation, traversal, and deletion
        Part III: OSP - Walker and node fundamentals
        Build an AI Day Planner - Full tutorial using these patterns

The .reports Array#

Every time a walker executes a report statement, the value is appended to a .reports array. When you spawn a walker, you receive this array in the response.

walker:priv MyWalker {
    
can do_work with Root entry {
        
report "first";   # reports[0]
        
report "second";  # reports[1]
    
}
}

with entry {
    
# Spawning the walker
    
response = root spawn MyWalker();
    
print(response.reports);  # ["first", "second"]
}

Common Patterns#
Pattern 1: Single Report (Recommended)#

The cleanest pattern accumulates data internally and reports once at the end:

node Item {
    
has data: str;
}

walker:priv ListItems {
    
has items: list = [];

    
can collect with Root entry {
        
visit [-->];
    
}

    
can gather with Item entry {
        
self.items.append(here.data);
    
}

    
can finish with Root exit {
        
report self.items;  # Single report with all data
    
}
}

with entry {
    
# Usage
    
result = root spawn ListItems();
    
items = result.reports[0];  # The complete list
}

When to use: Most read operations, listing data, aggregations.

This is the accumulator pattern -- the standard approach for collecting data from a graph traversal. The walker flows through three stages:

    Enter root → initiate traversal with visit [-->]
    Visit each node → gather data into walker state (self.items)
    Exit root → report the accumulated result

The with Root exit ability fires after the walker has finished visiting all queued nodes and returns to root, making it the ideal place for a single consolidated report.

Accumulator in Frontend

When calling this pattern from client code, access the result with result.reports[0] -- there is always exactly one report containing the full collection.

For a complete walkthrough of this pattern in a full-stack app, see Build an AI Day Planner.
Pattern 2: Report Per Node#

Reports each item as it's found during traversal:

node Item {
    
has name: str;
}

walker:priv FindMatches {
    
has search_term: str;

    
can search with Root entry {
        
visit [-->];
    
}

    
can check with Item entry {
        
if self.search_term in here.name {
            
report here;  # One report per match
        
}
    
}
}

with entry {
    
# Usage
    
result = root spawn FindMatches(search_term="test");
    
matches = result.reports;  # Array of all matching nodes
}

When to use: Search operations, filtering, finding specific nodes.
Pattern 3: Operation + Result#

Performs an operation and reports a summary:

node Item {
    
has name: str;
}

walker:priv CreateItem {
    
has name: str;

    
can create with Root entry {
        
new_item = here ++> Item(name=self.name);
        
report new_item[0];  # Report the created item
    
}
}

with entry {
    
# Usage
    
result = root spawn CreateItem(name="New Item");
    
created = result.reports[0];  # The new item
}

When to use: Create, update, delete operations.
Pattern 4: Nested Walker Spawning#

When one walker spawns another, use has attributes to pass data between them instead of relying on reports:

walker:priv InnerWalker {
    
has result: str = "";

    
can work with Root entry {
        
self.result = "inner data";
    
}
}

walker:priv OuterWalker {
    
can work with Root entry {
        
# Spawn inner walker
        
inner = InnerWalker();
        
root spawn inner;

        
# Access inner walker's data via its attributes
        
report {"outer": "data", "inner": inner.result};
    
}
}

with entry {
    
# Usage
    
result = root spawn OuterWalker();
    
# result.reports[0] = {"outer": "data", "inner": "inner data"}
}

Important: When spawning walkers from within other walkers, the inner walker's reports list may not be accessible from the parent context. Use has attributes on the inner walker to communicate results back to the outer walker.
Pattern 5: Multiple Reports (Complex Operations)#

Some operations naturally produce multiple reports:

def do_processing(input: str) -> list {
    
return [input, input + "_processed"];
}

walker:priv ProcessAndSummarize {
    
has input: str;

    
can process with Root entry {
        
# First report: raw results
        
results = do_processing(self.input);
        
report results;

        
# Second report: summary
        
report {
            
"count": len(results),
            
"status": "complete"
        
};
    
}
}

with entry {
    
# Usage
    
result = root spawn ProcessAndSummarize(input="data");
    
raw_results = result.reports[0];  # First report
    
summary = result.reports[1];       # Second report
}

When to use: Operations that produce both detailed results and summaries.
Safe Access Patterns#

Always handle the possibility of empty reports:

walker:priv MyWalker {
    
can work with Root entry {
        
report "data";
    
}
}

def process(item: any) {
    
print(item);
}

with entry {
    
# Safe single report access
    
result = root spawn MyWalker();
    
data = result.reports[0] if result.reports else None;

    
# Safe with default value
    
data = result.reports[0] if result.reports else [];

    
# Check length for multiple reports
    
if result.reports and len(result.reports) > 1 {
        
first = result.reports[0];
        
second = result.reports[1];
    
}

    
# Iterate all reports
    
for item in (result.reports if result.reports else []) {
        
process(item);
    
}
}

Response Object Structure#

The full response object from root spawn Walker():

walker:priv MyWalker {
    
can work with Root entry {
        
report "result";
    
}
}

with entry {
    
response = root spawn MyWalker();

    
# Available properties
    
print(response.reports);    # Array of all reported values
}

Best Practices#

    Prefer single reports - Accumulate data and report once at the end
    Use with Root exit - Best place for final reports after traversal
    Document report structure - Comment what each report index contains
    Always check .reports - It may be empty or undefined
    Keep reports serializable - Stick to dicts, lists, strings, numbers, bools

Anti-Patterns#
Don't: Report in a loop without accumulation#

node Item {
    
has data: str;
}

# Bad: Creates many small reports
walker:priv BadPattern {
    
can process with Item entry {
        
report here.data;  # N reports for N items
    
}
}

# Good: Accumulate and report once
walker:priv GoodPattern {
    
has items: list = [];

    
can start with Root entry {
        
visit [-->];
    
}

    
can process with Item entry {
        
self.items.append(here.data);
    
}

    
can finish with Root exit {
        
report self.items;  # One report with all items
    
}
}

Don't: Assume report order without documentation#

walker:priv MyWalker {
    
can work with Root entry {
        
report ["item1", "item2"];
        
report {"count": 2};
    
}
}

with entry {
    
result = root spawn MyWalker();

    
# Bad: Magic indices
    
data = result.reports[0];
    
meta = result.reports[1];

    
# Good: Document or structure clearly
    
# reports[0]: List of items
    
# reports[1]: Metadata object
    
data = result.reports[0] if result.reports else [];
    
meta = result.reports[1] if len(result.reports) > 1 else {};
}

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.


Skip to content
logo
Jac - AI-Native Full-Stack Development
Appendices
Type to start searching
GitHub

    v2.3.2
    450
    355

    Get Started
    Full Reference
    Community
    Showcase

    Full Reference
        Overview
        Language Specification
        AI Integration
        Full-Stack Development
        Deployment & Scaling
        Developer Workflow
        Python Integration
        Quick Reference
            Walker Patterns
            Appendices

Table of contents

    Appendix A: Complete Keyword Reference
    Appendix B: Operator Quick Reference
        Arithmetic
        Comparison
        Logical
        Graph (OSP)
        Pipe
    Appendix C: Grammar Summary
    Appendix D: Common Gotchas
        1. Semicolons Required
        2. Braces Required for Blocks
        3. Type Annotations Required
        4. has vs Local Variables
        5. Walker visit is Queued
        6. report vs return
        7. Global Modification Requires Declaration
    Appendix E: Migration from Python
        Quick Reference Table
        Class to Object
        Function
        Control Flow
        Imports
        Enums
        Entry Point
        Module-Level Variables
        Error Handling
    Appendix F: LLM Provider Reference
    Document Information

    Full Reference
    Quick Reference

Appendices#

In this part:

    Appendix A: Complete Keyword Reference - All keywords
    Appendix B: Operator Quick Reference - Operators by category
    Appendix C: Grammar Summary - Simplified grammar
    Appendix D: Common Gotchas - Pitfalls to avoid
    Appendix E: Migration from Python - Conversion guide
    Appendix F: LLM Provider Reference - Model configuration

Appendix A: Complete Keyword Reference#
Keyword 	Category 	Description
abs 	Modifier 	Abstract method/class (note: NOT abstract)
and 	Operator 	Logical AND (also &&)
as 	Import 	Alias
assert 	Statement 	Assertion
async 	Modifier 	Async function/walker
await 	Expression 	Await async
break 	Control 	Exit loop
by 	Operator 	Delegation operator (used by byllm for LLM)
can 	Declaration 	Ability (method on archetypes)
case 	Control 	Match/switch case
cl 	Block 	Client-side code block
na 	Block 	Native code block (compiles to LLVM IR)
class 	Archetype 	Python-style class definition
continue 	Control 	Next iteration
def 	Declaration 	Function
default 	Control 	Switch default case
del 	Statement 	Delete node/edge
disengage 	OSP 	Stop walker traversal
edge 	Archetype 	Edge type
elif 	Control 	Else if
else 	Control 	Else branch
entry 	OSP 	Entry event trigger
enum 	Archetype 	Enumeration
except 	Control 	Exception handler
exit 	OSP 	Exit event trigger
finally 	Control 	Finally block
flow 	Concurrency 	Start concurrent task
for 	Control 	For loop
from 	Import 	Import from
glob 	Declaration 	Global variable
global 	Scope 	Access global scope
has 	Declaration 	Instance field
here 	OSP 	Current node (in walker)
if 	Control 	Conditional
impl 	Declaration 	Implementation block
import 	Module 	Import
in 	Operator 	Membership
include 	Module 	Include/merge code
init 	Method 	Constructor
is 	Operator 	Identity
lambda 	Expression 	Anonymous function
match 	Control 	Pattern match
node 	Archetype 	Node type
nonlocal 	Scope 	Access nonlocal scope
not 	Operator 	Logical NOT
obj 	Archetype 	Object/class
or 	Operator 	Logical OR (also \|\|)
override 	Modifier 	Override method
postinit 	Method 	Post-constructor
priv 	Access 	Private
props 	Reference 	JSX props (client-side)
protect 	Access 	Protected
pub 	Access 	Public
raise 	Statement 	Raise exception
report 	OSP 	Report value from walker
return 	Statement 	Return value
root 	OSP 	Root node reference
self 	Reference 	Current instance
sem 	Declaration 	Semantic string
skip 	Control 	Skip (nested context)
spawn 	OSP 	Spawn walker
static 	Modifier 	Static member
super 	Reference 	Parent class
sv 	Block 	Server-side code block
switch 	Control 	Switch statement
test 	Declaration 	Test block
to 	Control 	For loop upper bound
try 	Control 	Try block
visitor 	OSP 	Visiting walker (in node)
wait 	Concurrency 	Wait for concurrent result
walker 	Archetype 	Walker type
while 	Control 	While loop
with 	Statement 	Context manager / entry block
yield 	Statement 	Generator yield

Notes:

    The abstract keyword is abs, not abstract
    Logical operators have both word and symbol forms: and/&&, or/||
    cl, sv, and na are block keywords for client/server/native code separation

Appendix B: Operator Quick Reference#
Arithmetic#
Operator 	Description
+ 	Addition
- 	Subtraction
* 	Multiplication
/ 	Division
// 	Floor division
% 	Modulo
** 	Power
Comparison#
Operator 	Description
== 	Equal
!= 	Not equal
< 	Less than
> 	Greater than
<= 	Less or equal
>= 	Greater or equal
Logical#
Operator 	Description
and, && 	Logical AND
or, \|\| 	Logical OR
not 	Logical NOT
Graph (OSP)#
Operator 	Description
++> 	Forward connect
<++ 	Backward connect
<++> 	Bidirectional connect
+>:T:+> 	Typed forward
<+:T:<+ 	Typed backward
<+:T:+> 	Typed bidirectional
[-->] 	Outgoing edges
[<--] 	Incoming edges
[<-->] 	All edges
Pipe#
Operator 	Description
\|> 	Forward pipe
<\| 	Backward pipe
:> 	Atomic forward
<: 	Atomic backward
Appendix C: Grammar Summary#

module        : STRING? element*              # Optional module docstring
element       : STRING? toplevel_stmt         # Optional statement docstring
toplevel_stmt : import | archetype | ability | impl | test | entry
              | (cl | sv | na) toplevel_stmt       # Client/server/native prefix
              | (cl | sv | na) "{" toplevel_stmt* "}"  # Client/server/native block

archetype     : async? (obj | node | edge | walker | enum) NAME inheritance? body
inheritance   : "(" NAME ("," NAME)* ")"
body          : "{" member* "}"

member        : has_stmt | ability | impl
has_stmt      : "has" (modifier)? NAME ":" type ("=" expr)? ";"
ability       : async? "can" NAME params? ("->" type)? event_clause? (body | ";")
event_clause  : "with" type_expr? (entry | exit)

import        : "import" (module | "from" import_path "{" names "}")
              | "import" "from" STRING "{" extern_decl* "}"  # C library import (na)
import_path   : (NAME ":")? dotted_name       # Optional namespace prefix (e.g., jac:module)
entry         : "with" "entry" (":" NAME)? body
test          : "test" NAME body
impl          : "impl" NAME "." NAME params body

visit_stmt    : "visit" (":" expr ":")? expr ("else" block)?  # Optional index selector
edge_ref      : "[" (edge | node)? edge_op filter? "]"

expr          : ... (standard expressions plus graph operators)

# Pattern matching
match_stmt    : "match" expr "{" case_clause* "}"
case_clause   : "case" pattern ":" stmt*
pattern       : literal | capture | sequence | mapping | class | as | or | star

Appendix D: Common Gotchas#
1. Semicolons Required#

# Wrong - missing semicolons
# x = 5
# print(x)

# Correct
with entry {
    
x = 5;
    
print(x);
}

2. Braces Required for Blocks#

# Wrong (Python style) - won't parse
# if condition:
#     do_something()

# Correct
def do_something() -> None {
    
print("done");
}

with entry {
    
condition = True;
    
if condition {
        
do_something();
    
}
}

3. Type Annotations Required#

# Wrong - missing type annotations
# def add(a, b) {
#     return a + b;
# }

# Correct
def add(a: int, b: int) -> int {
    
return a + b;
}

4. has vs Local Variables#

obj Example {
    
has field: int = 0;  # Instance variable (with 'has')

    
def method() {
        
local = 5;  # Local variable (no 'has')
        
self.field = local;
    
}
}

5. Walker visit is Queued#

walker Example {
    
can traverse with Node entry {
        
print("Visiting");
        
visit [-->];  # Nodes queued, visited AFTER this method
        
print("This prints before visiting children");
    
}
}

6. report vs return#

walker Example {
    
can collect with Node entry {
        
report here.value;  # Continues execution
        
visit [-->];        # Still runs

        
return here.value;  # Would stop here
    
}
}

7. Global Modification Requires Declaration#

glob counter: int = 0;

def increment -> None {
    
global counter;  # Required!
    
counter += 1;
}

Appendix E: Migration from Python#
Quick Reference Table#
Concept 	Python 	Jac
Code blocks 	Indentation 	{ } braces
Statements 	No semicolons 	; required
Classes 	class Foo: 	obj Foo { }
Attributes 	self.x = val in __init__ 	has x: type = val;
Methods 	def method(self): 	def method() { } (self is implicit)
Entry point 	if __name__ == "__main__": 	with entry { }
Module variables 	Global assignment 	glob keyword
Enums 	class Color(Enum): 	enum Color { RED, GREEN, BLUE }
Error handling 	try: ... except: 	try { } except Type as e { }
Imports 	from x import y 	import from x { y }
Pattern matching 	match x: case 1: 	match x { case 1: (Python-style indentation inside braces)
Inheritance 	class Dog(Animal): 	obj Dog(Animal) { }

Match Case Syntax

Match case bodies use Python-style indentation (not braces), even though they appear inside a braces-delimited block. This is unique in Jac.
Class to Object#

Python:

class Person:
    
def __init__(self, name: str, age: int):
        
self.name = name
        
self.age = age

    
def greet(self) -> str:
        
return f"Hi, I'm {self.name}"

Jac:

obj Person {
    
has name: str;
    
has age: int;

    
def greet() -> str {
        
return f"Hi, I'm {self.name}";
    
}
}

with entry {
    
p = Person(name="Alice", age=30);
}

Function#

Python:

def add(a: int, b: int) -> int:
    
return a + b

Jac:

def add(a: int, b: int) -> int {
    
return a + b;
}

Control Flow#

Python:

if x > 0:
    
print("positive")
elif x < 0:
    
print("negative")
else:
    
print("zero")

Jac:

with entry {
    
x = 1;
    
if x > 0 {
        
print("positive");
    
} elif x < 0 {
        
print("negative");
    
} else {
        
print("zero");
    
}
}

Imports#

Python:

import math
from collections import Counter, defaultdict

Jac:

import math;
import from collections { Counter, defaultdict }

Enums#

Python:

from enum import Enum

class Status(Enum):
    
PENDING = "pending"
    
ACTIVE = "active"

Jac:

enum Status {
    
PENDING = "pending",
    
ACTIVE = "active"
}

Entry Point#

Python:

if __name__ == "__main__":
    
main()

Jac:

with entry {
    
main();
}

Module-Level Variables#

Python:

config = {"debug": True, "version": "1.0.0"}

Jac:

glob config: dict = {"debug": True, "version": "1.0.0"};

Error Handling#

Python:

try:
    
result = divide(10, 0)
except ValueError as e:
    
print(f"Error: {e}")
finally:
    
print("Done")

Jac:

try {
    
result = divide(10, 0);
} except ValueError as e {
    
print(f"Error: {e}");
} finally {
    
print("Done");
}

For a step-by-step transition guide, see Jac Basics Tutorial.
Appendix F: LLM Provider Reference#
Provider 	Model Names 	Environment Variable
OpenAI 	gpt-4, gpt-4o, gpt-3.5-turbo 	OPENAI_API_KEY
Anthropic 	claude-3-opus, claude-3-sonnet 	ANTHROPIC_API_KEY
Google 	gemini-pro, gemini-ultra 	GOOGLE_API_KEY
Azure 	azure/gpt-4 	Azure config
Ollama 	ollama/llama2, ollama/mistral 	Local (no key)

Model Name Format:

provider/model-name

Examples:
- gpt-4 (OpenAI, default provider)
- anthropic/claude-3-opus
- azure/gpt-4
- ollama/llama2

Document Information#

Jac Language Reference

Version: 3.1 Last Updated: January 2026

Validation Status: Validated against the Jac recursive descent parser (jaclang 0.10.0)

Resources:

    Website: https://jaseci.org
    Documentation: https://jac-lang.org
    GitHub: https://github.com/Jaseci-Labs/jaseci
    Discord: https://discord.gg/6j3QNdtcN6

Jac

Built with passion for innovative programming languages
Resources

    Quick Guide
    Tutorials
    Language Reference

Community

    GitHub
    Discord
    Discussions

Connect

© 2026 Jac Hackers Everywhere. All rights reserved.
