from testing.agent import SQLTutorAgent

agent = SQLTutorAgent()

report = agent.create_learning_report(72)

print(report)