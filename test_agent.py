from testing.agent import SQLTutorAgent


if __name__ == "__main__":
    agent = SQLTutorAgent()
    report = agent.create_learning_report(72)
    print(report)
