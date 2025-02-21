import os
import json
import streamlit as st
from typing import Union, List, Tuple, Dict
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.parser import AgentFinish



@CrewBase
class CodeReviewCrew:
    """Code Review Crew extended for defects review, refactoring and code completions."""
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def step_callback(
        self,
        agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish],  
        agent_name: str,
        *args,
    ):
        """Callback function to handle the output of the agents."""
        with st.chat_message("AI"):
            if isinstance(agent_output, str):
                try:
                    # Try to parse the output as JSON
                    agent_output = json.loads(agent_output) 
                except json.JSONDecodeError:
                    pass
                
            # If the agent has finished processing show the output
            if isinstance(agent_output, AgentFinish):   
                st.write(f" {agent_name} has finished processing.")
                with st.expander("Show Output"):
                    st.write(f"{getattr(agent_output, 'output', 'Unknown')}")   

            else:
                st.write(f"Unexpected output type: {type(agent_output)}")
                st.write(agent_output)

    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["code_reviewer"],
            verbose=True,
            step_callback=lambda output, agent_name="Reviewer Agent", *args: self.step_callback(output, agent_name, *args)
        )
    
    @agent
    def code_completer(self) -> Agent:
        return Agent(
            config=self.agents_config["code_completer"],
            verbose=True,
            step_callback=lambda output, agent_name="Coder Agent", *args: self.step_callback(output, agent_name, *args)

        )

    @task
    def review_code(self) -> Task:
        return Task(
            config=self.tasks_config["review_code"],
            output_file="review_output.md"
        )
    
    @task
    def code_completion(self) -> Task:
        return Task(
            config=self.tasks_config["code_completion"],
            output_file="completion_output.md"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,    # it remembers the contexts within same session
        )
