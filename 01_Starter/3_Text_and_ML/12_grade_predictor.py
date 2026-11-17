"""
12 - Grade predictor (linear regression)
----------------------------------------
Hours of study -> predicted grade (out of 6, Swiss style).
The model draws the best straight line through the points: that's "linear regression".

Run:  python 12_grade_predictor.py
Try:  change the data with your own class results. What happens with 20 hours? Is it realistic?
"""

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

hours = [[0], [1], [2], [3], [4], [5], [6], [8]]     # inputs: a list of lists (1 column)
grades = [2.5, 3.0, 3.5, 4.0, 4.3, 4.8, 5.2, 5.8]    # answers

model = LinearRegression().fit(hours, grades)         # find the best line

h = float(input("How many hours did you study? "))
print(f"Predicted grade: {model.predict([[h]])[0]:.1f} / 6")
print(f"(each extra hour adds about {model.coef_[0]:.2f} points)")  # the slope of the line

# Draw the points and the line
plt.scatter([x[0] for x in hours], grades, label="real students")
plt.plot([0, 8], model.predict([[0], [8]]), color="red", label="model's line")
plt.xlabel("Hours of study")
plt.ylabel("Grade")
plt.legend()
plt.show()
