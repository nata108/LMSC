import numpy as np
from taskweaver.plugin import Plugin, register_plugin
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import io

@register_plugin
class ThreeBodyPlugin(Plugin):
    def __call__(self, mass1, mass2, mass3,
                 pos1, pos2, pos3,
                 vel1, vel2, vel3,
                 total_time, time_step):
        """
        Simulates the three-body problem and returns a GIF of the simulation.

        :param mass1: Mass of body 1.
        :param mass2: Mass of body 2.
        :param mass3: Mass of body 3.
        :param pos1: Initial position of body 1 as a tuple (x, y).
        :param pos2: Initial position of body 2 as a tuple (x, y).
        :param pos3: Initial position of body 3 as a tuple (x, y).
        :param vel1: Initial velocity of body 1 as a tuple (vx, vy).
        :param vel2: Initial velocity of body 2 as a tuple (vx, vy).
        :param vel3: Initial velocity of body 3 as a tuple (vx, vy).
        :param total_time: Total simulation time.
        :param time_step: Time step for the simulation.
        :param output_path: Path to save the output GIF.
        
        :return: PIL Image of the simulation GIF.
        """
        try:
            # Initialize positions and velocities
            positions = np.array([pos1, pos2, pos3], dtype='float64')
            velocities = np.array([vel1, vel2, vel3], dtype='float64')
            # use megaton as the unit of mass
            masses = np.array([mass1, mass2, mass3], dtype='float64')*1e9
            G = 6.67430e-11  # Gravitational constant

            num_steps = int(total_time / time_step)
            traj = {0: [positions[0].copy()],
                    1: [positions[1].copy()],
                    2: [positions[2].copy()]}
            traj_forces = {0: [], 1: [], 2: []}  # Add force trajectories

            for _ in range(num_steps):
                # Calculate pairwise forces
                forces = np.zeros((3, 2))  # Initialize forces array
                for i in range(3):
                    force = np.zeros(2)
                    for j in range(3):
                        if i != j:
                            r = positions[j] - positions[i]
                            distance = np.linalg.norm(r) + 1e-10  # Prevent division by zero
                            force += G * masses[j] * r / distance**3
                    forces[i] = force  # Store force on body i
                    velocities[i] += force * time_step
                # Update positions
                positions += velocities * time_step
                # Record trajectories
                for i in range(3):
                    traj[i].append(positions[i].copy())
                    traj_forces[i].append(forces[i].copy())  # Record forces

            # Create animation
            fig, ax = plt.subplots()
            colors = ['r', 'g', 'b']
            lines = [ax.plot([], [], 'o', color=colors[i])[0] for i in range(3)]
            forces_lines = [ax.quiver([], [], [], [], color=colors[i]) for i in range(3)]  # Add force quivers

            def init():
                ax.set_xlim(max(np.min([traj[i][k][0] for i in traj for k in range(len(traj[i]))]) - 1,-300),
                            min(np.max([traj[i][k][0] for i in traj for k in range(len(traj[i]))]) + 1,300))
                ax.set_ylim(max(np.min([traj[i][k][1] for i in traj for k in range(len(traj[i]))]) - 1,-300),
                            min(np.max([traj[i][k][1] for i in traj for k in range(len(traj[i]))]) + 1,300))
                for q in forces_lines:
                    q.set_UVC([], [])
                return lines + forces_lines

            def update(frame):
                for i, line in enumerate(lines):
                    line.set_data([traj[i][frame][0]], [traj[i][frame][1]])
                for i, q in enumerate(forces_lines):
                    force = traj_forces[i][frame]
                    magnitude = np.linalg.norm(force)
                    if magnitude > 2:
                        force = force / magnitude * 2
                    elif magnitude < 0:
                        force = np.array([0, 0])
                    q.set_offsets([traj[i][frame][0], traj[i][frame][1]])
                    q.set_UVC(force[0], force[1])
                return lines + forces_lines

            anim = FuncAnimation(fig, update, frames=num_steps, init_func=init, blit=True)
            anim.save("temp.gif", writer='imagemagick', fps=30)
            plt.close(fig)

            return "temp.gif"

        except Exception as e:
            raise e

if __name__ == "__main__":
    from taskweaver.plugin.context import temp_context
    with temp_context() as temp_ctx:
        # Test the plugin
        plugin = ThreeBodyPlugin(name="threebody", ctx=temp_ctx, config={})

        mass1, mass2, mass3 = 10000, 300, 100
        pos1, pos2, pos3 = (0, 0), (100, 0), (50, np.sqrt(3)/2*100)
        vel1, vel2, vel3 = (0.1, 0.1), (0, np.sqrt(3)/2*2), (-np.sqrt(3)/2*2, 0)
        total_time, time_step = 500, 1.0

        # Run the simulation
        gif_path = plugin(mass1, mass2, mass3, pos1, pos2, pos3, vel1, vel2, vel3, total_time, time_step)