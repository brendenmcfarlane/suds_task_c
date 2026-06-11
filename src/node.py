from src.agent import Agent

class AgentNode:
    def __init__(self, agent):
        self._agent = agent
        self._is_informed = False
        self._N_out = []
        self._N_in = []
        self._messages = []
        self._output = None

    def get_agent_name(self):
        return self._agent.get_name()
    
    def get_output(self):
        return self._output
    
    def get_outgoing(self):
        return self._N_out
    
    def get_incoming(self):
        return self._N_in
    
    def check_informed(self):
        self._is_informed = (len(self._N_in) == len(self._messages))
        return self._is_informed
    
    def receive_message(self, message):
        self._messages.append(message)

    def add_outgoing(self, node):
        self._N_out.append(node)

    def add_incoming(self, node):
        self._N_in.append(node)

    def call_agent(self):
        self._output = self._agent.call(" ".join(self._messages))

class QuestionNode(AgentNode):
    def __init__(self):
        super().__init__(Agent("QuestionNode"))
        self._is_informed = True
        self._output = ""
    
    def set_question(self, question):
        self._output = question

    def add_incoming(self, node):
        raise Exception("QuestionNode cannot have incoming edges.")
    
    def receive_message(self, message):
        raise Exception("QuestionNode cannot receive messages.")
    
    def call_agent(self):
        pass

class SinkNode(AgentNode):
    def __init__(self):
        super().__init__(Agent("SinkNode", ""))       
        self._output = None

    def add_outgoing(self, node):
        raise Exception("SinkNode cannot have outgoing edges.")
    
    def receive_message(self, message):
        self._messages.append(message)
        self._output = message

    def call_agent(self):
        return self._output

    

def main():
    pass
    agent = Agent("buddy", "What is the meaning of life?")
    node = AgentNode(agent)
    node2 = AgentNode(Agent("friend", "What is the meaning of life?"))
    node.add_outgoing(node2)
    print (node.get_agent_name())
    print (node.check_informed())
    node.add_incoming("messenger1")
    print (node.check_informed())
    print (node._output)
    print (node2._messages)
    node.call_agent()
    print (node._output)
    print (node2._messages)


if __name__ == "__main__":    main()