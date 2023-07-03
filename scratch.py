import matplotlib.pyplot as plt

WIDTH,HEIGHT = 10, 6
# Example data
categories = ['A', 'B', 'C', 'D']
values = [10, 20, 15, 25]

fig, ax = plt.subplots(figsize = (WIDTH,HEIGHT))
# Create horizontal bar chart
ax.barh(categories, values)

# Add labels and title
ax.set_xlabel('Values')
ax.set_ylabel('Categories')
ax.set_title('Rotated Bar Chart')

for i, value in enumerate(values):
    plt.text(value, i, str(value), va='center')

# Show the chart
plt.show()
