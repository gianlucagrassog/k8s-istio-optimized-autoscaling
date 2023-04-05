import numpy as np
import matplotlib.pyplot as plt

# Set the random seed for reproducibility
np.random.seed(42)

# Generate 1000 samples from an exponential distribution with lambda=0.2
lam = 0.2
data = np.random.exponential(scale=1/lam, size=10000)

# Plot the PDF of the exponential distribution
plt.figure(figsize=(8, 5))
x = np.linspace(0, 40, 100)
pdf = lam * np.exp(-lam * x)

plt.hist(data, bins=200, density=True, alpha=0.5)
plt.plot(x, pdf, 'r', lw=2)
plt.xlabel('x')
plt.ylabel('Probability density')
plt.title('Exponential distribution PDF with $\lambda$ = {}'.format(lam))

# Show the plot PDF
plt.show()

# Plot the CDF of the exponential distribution
plt.figure(figsize=(8, 5))
cdf = 1 - np.exp(-lam * x)


plt.plot(x, cdf, 'g', lw=2)
plt.xlabel('x')
plt.ylabel('Cumulative probability')
plt.title('Exponential distribution CDF with $\lambda$ = {}'.format(lam))

# Show the plot CDF
plt.show()
