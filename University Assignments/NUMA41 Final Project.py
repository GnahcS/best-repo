import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Constants
g = 9.81
l = 1.0
alpha_obst = -np.pi/6


# Perform one time step using trapezoidal rule with Newton's method.
def trapezoidal_step_newton(alpha_n, omega_n, h, max_iter=20, tol=1e-10):
    # Initial guess: explicit Euler predictor
    alpha_guess = alpha_n + h * omega_n
    omega_guess = omega_n - h * (g/l) * np.sin(alpha_n)
    
    # Newton iteration
    for k in range(max_iter):
        # Compute residuals F1, F2
        F1 = alpha_guess - alpha_n - (h/2) * (omega_n + omega_guess)
        F2 = omega_guess - omega_n + (h*g/(2*l)) * (np.sin(alpha_n) + np.sin(alpha_guess))
        
        # Compute Jacobian determinant
        cos_alpha = np.cos(alpha_guess)
        det = 1 + (h**2 * g / (4*l)) * cos_alpha
        
        # Compute corrections using explicit 2x2 solution
        delta_alpha = (-F1 - (h/2) * F2) / det
        delta_omega = (-F2 + (h*g/(2*l)) * cos_alpha * F1) / det
        
        # Update guess
        alpha_guess += delta_alpha
        omega_guess += delta_omega
        
        # Check convergence
        norm_delta = np.sqrt(delta_alpha**2 + delta_omega**2)
        if norm_delta < tol:
            break
    
    return alpha_guess, omega_guess

# Quadratic interpolation function for three data points
def interpolate_quadratic(triple_t, triple_y):
    # Unpack inputs
    t0, t1, t2 = triple_t
    y0, y1, y2 = triple_y  # each y is [alpha, omega]
    
    # Separate angle and angular velocity data
    alpha_data = [y0[0], y1[0], y2[0]]
    omega_data = [y0[1], y1[1], y2[1]]
    
    # Denominators for Lagrange basis polynomials
    denom01 = (t0 - t1) * (t0 - t2)
    denom02 = (t1 - t0) * (t1 - t2)
    denom03 = (t2 - t0) * (t2 - t1)
    
    def p_alpha(t):
        # Quadratic polynomial interpolating angle α
        L0 = (t - t1) * (t - t2) / denom01
        L1 = (t - t0) * (t - t2) / denom02
        L2 = (t - t0) * (t - t1) / denom03
        return alpha_data[0] * L0 + alpha_data[1] * L1 + alpha_data[2] * L2
    
    def p_omega(t):
        # Quadratic polynomial interpolating angular velocity ω
        L0 = (t - t1) * (t - t2) / denom01
        L1 = (t - t0) * (t - t2) / denom02
        L2 = (t - t0) * (t - t1) / denom03
        return omega_data[0] * L0 + omega_data[1] * L1 + omega_data[2] * L2
    
    def p(t):
        # Vector-valued interpolation function.
        return np.array([p_alpha(t), p_omega(t)])
    
    return p

# Check if pendulum passed obstacle
def detect_obstacle_crossing(t_n, t_n_plus1, p_func, alpha_obst=-np.pi/6, tol=1e-10): 
    # Get p_alpha values at interval endpoints
    alpha_at_n = p_func(t_n)[0]
    alpha_at_n_plus1 = p_func(t_n_plus1)[0]
    
    if (alpha_at_n - alpha_obst) * (alpha_at_n_plus1 - alpha_obst) > 0:
        # Both endpoints on same side of obstacle → no crossing
        return False, None
    
    # Bisection
    a, b = t_n, t_n_plus1
    f_a = alpha_at_n - alpha_obst
    f_b = alpha_at_n_plus1 - alpha_obst
    
    # Ensure f(a) and f(b) have opposite signs
    if f_a * f_b > 0:
        # Could be touching at endpoint
        if abs(f_a) < tol:
            return True, t_n
        elif abs(f_b) < tol:
            return True, t_n_plus1
        else:
            return False, None
    
    # Bisection to find root
    for _ in range(30):  # 30 iterations → accuracy ~ 1e-9
        t_mid = (a + b) / 2
        f_mid = p_func(t_mid)[0] - alpha_obst
        
        if abs(f_mid) < tol:
            return True, t_mid
        
        if f_a * f_mid <= 0:
            b = t_mid
            f_b = f_mid
        else:
            a = t_mid
            f_a = f_mid
    
    t_obst = (a + b) / 2
    return True, t_obst


# Compute α_obst and ω_obst at collision time
def compute_obstacle_state(t_obst, p_func, alpha_obst=-np.pi/6):
    # Evaluate interpolation polynomial at t_obst
    alpha_at_impact, omega_at_impact = p_func(t_obst)
    
    return alpha_at_impact, omega_at_impact



# Pendulum integration function
def integrate_pendulum(t_end=5.0, h=0.01, obstacle_enabled=False):

    # Initial conditions
    t_current = 0.0
    alpha_current = np.pi/2
    omega_current = 0.0

    # No Obstacle
    if not obstacle_enabled:
        # Storage
        n_steps = int(np.ceil(t_end / h)) + 1
        t = np.zeros(n_steps)
        alpha = np.zeros(n_steps)
        omega = np.zeros(n_steps)
        
        t[0] = t_current 
        alpha[0] = alpha_current
        omega[0] = omega_current
        
        for n in range(n_steps - 1):
            alpha_next, omega_next = trapezoidal_step_newton(alpha[n], omega[n], h)
            t[n+1] = t[n] + h
            alpha[n+1] = alpha_next
            omega[n+1] = omega_next
        
        return t, alpha, omega, None
    
    # With Obstacle
    else:
        # Storage
        t_list = []
        alpha_list = []
        omega_list = []
        obstacle_events = []
        
        # Separate storage for last 3 points (for interpolation)
        # This gets reset after bounce.
        recent_t = []  
        recent_y = []
        
        # Counter fix for duplicate times 
        steps_since_bounce = 0
        
        while t_current < t_end:
            # Store current point in MAIN lists
            t_list.append(t_current)
            alpha_list.append(alpha_current)
            omega_list.append(omega_current)
            
            # Add to recent buffer
            recent_t.append(t_current)
            recent_y.append([alpha_current, omega_current])
            if len(recent_t) > 3:
                recent_t.pop(0)
                recent_y.pop(0)
            
            # Take one step
            alpha_next, omega_next = trapezoidal_step_newton(alpha_current, omega_current, h)
            t_next = t_current + h
            
            # Increment counter
            steps_since_bounce += 1
            
            # ===== OBSTACLE DETECTION =====
            # FIX: Need at least 3 points in recent buffer AND
            # wait at least 2 steps after bounce to avoid duplicate times
            if len(recent_t) == 3 and steps_since_bounce >= 2:
                # FIX: Check if times are DISTINCT (not duplicates)
                # This happens right after bounce when we store same point multiple times
                if len(set([round(t, 10) for t in recent_t])) == 3:
                    
                    # Create interpolation function from recent buffer
                    p_func = interpolate_quadratic(recent_t, recent_y)

                    # Check for obstacle crossing between last two points
                    hit, t_obst = detect_obstacle_crossing(recent_t[1], recent_t[2], p_func)
                    
                    if hit:
                        # Compute impact state
                        alpha_obst, omega_obst = compute_obstacle_state(t_obst, p_func)
                        
                        print(f"OBSTACLE HIT at t = {t_obst:.6f}")
                        print(f"  α at impact: {alpha_obst:.6f} rad")
                        print(f"  ω at impact: {omega_obst:.6f} rad/s")
                        print("\n")
            
                        # Record the event
                        event = {
                            't': t_obst,
                            'alpha': alpha_obst,
                            'omega': omega_obst,
                            'pre_bounce_omega': omega_obst
                        }
                        obstacle_events.append(event)
                            
                        # Store exact collision point
                        t_list.append(t_obst)
                        alpha_list.append(alpha_obst)
                        omega_list.append(omega_obst)
                        
                        print(f"Bounce! Restarting at t = {t_obst:.4f}s")
                        
                        # Set new inital conditions after bounce
                        t_current = t_obst
                        alpha_current = alpha_obst
                        omega_current = -omega_obst 
                        
                        # Reset RECENT buffer
                        recent_t = [t_current]
                        recent_y = [[alpha_current, omega_current]]
                        
                        # Reset counter
                        steps_since_bounce = 0
                        
                        # Skip normal update
                        continue
            
            # Update parameters
            t_current = t_next
            alpha_current = alpha_next
            omega_current = omega_next
        
        # Add final point
        t_list.append(t_current)
        alpha_list.append(alpha_current)
        omega_list.append(omega_current)
        
        return (
            np.array(t_list),
            np.array(alpha_list),
            np.array(omega_list),
            obstacle_events if obstacle_events else None
        )


# Plots
def no_obstacle_plot_angle(t, alpha):
    plt.figure(figsize=(10, 5))
    plt.plot(t, alpha, 'b-', linewidth=2)
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Angle α (rad)', fontsize=14)
    plt.title('Task 4: Pendulum Angle vs Time', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.show()


def no_obstacle_plot_velocity(t, omega):
    plt.figure(figsize=(10, 5))
    plt.plot(t, omega, 'r-', linewidth=2)
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Angular velocity ω (rad/s)', fontsize=14)
    plt.title('Task 4: Angular Velocity vs Time', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.show()


def obstacle_plot_angle(t, alpha, obstacle_events=None):
    plt.figure(figsize=(10, 4))
    plt.plot(t, alpha, 'b-')
    plt.axhline(y=-np.pi/6, color='red', linestyle='--')
    if obstacle_events:
        for event in obstacle_events:
            plt.axvline(x=event['t'], color='gray', linestyle=':')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle α (rad)')
    plt.title('Pendulum Angle vs Time with Obstacle')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def obstacle_plot_velocity(t, omega, obstacle_events=None):
    plt.figure(figsize=(10, 4))
    plt.plot(t, omega, 'r-')
    if obstacle_events:
        for event in obstacle_events:
            plt.axvline(x=event['t'], color='gray', linestyle=':')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular velocity ω (rad/s)')
    plt.title('Angular Velocity vs Time with Obstacle')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def obstacle_plot_phase(alpha, omega, obstacle_events=None):
    plt.figure(figsize=(8, 6))
    plt.plot(alpha, omega, 'b-')
    plt.axvline(x=-np.pi/6, color='red', linestyle='--')
    if obstacle_events:
        bounce_alphas = [e['alpha'] for e in obstacle_events]
        bounce_omegas = [e['omega'] for e in obstacle_events]
        plt.plot(bounce_alphas, bounce_omegas, 'ro')
    plt.xlabel('Angle α (rad)')
    plt.ylabel('Angular velocity ω (rad/s)')
    plt.title('Phase Plot with Obstacle')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Set parameters
    t_end = 5.0
    h = 0.01
    
    # Plots for Task 4
    t, alpha, omega, _ = integrate_pendulum(t_end=t_end, h=h, obstacle_enabled=False)
    no_obstacle_plot_angle(t, alpha)
    no_obstacle_plot_velocity(t, omega)

    # Plots for Task 12
    t, alpha, omega, events = integrate_pendulum(t_end=5.0, h=0.01, obstacle_enabled=True)
    obstacle_plot_angle(t, alpha, events)  # Shows kinks at bounces
    obstacle_plot_velocity(t, omega, events)  # Shows sign changes
    obstacle_plot_phase(alpha, omega, events)  # Shows bounce reflection