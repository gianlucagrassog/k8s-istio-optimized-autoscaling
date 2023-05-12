import seaborn as sns
import matplotlib.pyplot as plt

# Data
data = [56.59, 21.57, 15.25, 7]
labels = ['Checkout Service', 'Currency Service', 'Recommendation Service', 'Other Services']

data = [67.9, 12.3, 6.6,13.2]
labels = ['Frontend', 'Checkout Service', 'Currency Service', 'Other Services']

# Create pie chart
plt.figure(figsize=(6,4))
sns.set_palette("muted")

plt.pie(data, labels=labels, autopct='%1.1f%%')
plt.show()


plt.figure(figsize=(6,4))

sns.barplot(x=data, y=labels, palette="muted", orient='h')
plt.xlabel('Latency Contribution (%)')

plt.show()
