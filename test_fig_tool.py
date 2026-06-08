import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from crewai_book.tools.figure_generator_tool import FigureGeneratorTool

code = """
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Test Figure")
plt.savefig("test_fig.png")
"""

tool = FigureGeneratorTool()
print(tool._run(code, "test_fig.png"))
