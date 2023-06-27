from window import Window

def main():
    Window()

if __name__ == "__main__":
    main()

# import matplotlib.pyplot as plt
# import numpy as np
# import tkinter as tk
# from tkinter import ttk

# def random_walk_prob(p, step, N):
#     # Initialize the probability distribution
#     prob_dist = np.zeros((2 * N * step + 1,))

#     # Calculate the probabilities
#     prob_dist[N * step] = 1.0
#     for i in range(1, N + 1):
#         for j in range(1, step + 1):
#             prob_dist[N * step + i * step + j] = p * prob_dist[N * step + i * step + j - 1]
#             prob_dist[N * step - i * step - j] = (1 - p) * prob_dist[N * step - i * step - j + 1]

#     # Normalize the probabilities
#     prob_dist /= np.sum(prob_dist)

#     return prob_dist

# def plot_random_walk(p, step, N):
#     # Calculate the probability distribution
#     prob_dist = random_walk_prob(p, step, N)

#     # Generate the x-axis positions
#     positions = np.arange(-N * step, N * step + 1, step)

#     # Plot the probability distribution
#     plt.figure()
#     plt.bar(positions, prob_dist)
#     plt.xlabel('Position')
#     plt.ylabel('Probability')
#     plt.title('Probability Distribution of 1D Random Walk')
#     plt.show()

# def update_plot():
#     p = float(p_entry.get())
#     step = int(step_entry.get())
#     N = int(N_entry.get())
#     plot_random_walk(p, step, N)

# # Create GUI using Tkinter
# root = tk.Tk()
# root.title('1D Random Walk Probability Distribution')

# # Probability label and entry
# p_label = ttk.Label(root, text='Probability to Move Forward (p):')
# p_label.pack()
# p_entry = ttk.Entry(root)
# p_entry.pack()

# # Step size label and entry
# step_label = ttk.Label(root, text='Step Size:')
# step_label.pack()
# step_entry = ttk.Entry(root)
# step_entry.pack()

# # Number of iterations label and entry
# N_label = ttk.Label(root, text='Number of Iterations:')
# N_label.pack()
# N_entry = ttk.Entry(root)
# N_entry.pack()

# # Plot button
# plot_button = ttk.Button(root, text='Plot', command=update_plot)
# plot_button.pack()

# root.mainloop()

