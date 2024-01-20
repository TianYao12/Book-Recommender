from dotenv import load_dotenv
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.agents import tool, load_tools, initialize_agent, AgentType, AgentExecutor

load_dotenv(".env.local")

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

def create_agent():
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={
        'temperature': 0.6, 'max_length': 64
    })

    # Other tools: https://python.langchain.com/docs/integrations/tools/
    tools = load_tools(['wikipedia', 'llm-math'], llm=llm)

    # ReACT is a prompt template with "Thought, Observation, Action" stages
    # More details on ReACT (https://arxiv.org/abs/2210.03629)
    # Other agents (https://python.langchain.com/docs/modules/agents/agent_types/)
    agent = initialize_agent(tools=tools, llm=llm, verbose=True,
                             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    
    return agent

def get_answer(question):
    my_agent = create_agent()
    answer = my_agent.run(question)
    return answer

