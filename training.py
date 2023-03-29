from environment import TouhouEnvironment
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv
from mem_test import print_available_memory

low_mem = False

def main():
    # Initialize the custom environment
    print("Initializing environment...")
    env = TouhouEnvironment()

    # Wrap the environment in a DummyVecEnv for compatibility with stable-baselines3
    print("Wrapping environment...")
    env = DummyVecEnv([lambda: env])
    
    # Set up the PPO agent
    print("Setting up PPO agent...")
    if(low_mem):
        print_available_memory()
    model = PPO("MultiInputPolicy", env, n_steps=256, ent_coef=0.01, learning_rate=2.5e-4, n_epochs=4, clip_range=0.2, verbose=1)

    # Train the agent
    print("Training PPO agent...")
    total_timesteps = 1000000
    model.learn(total_timesteps)

    # Save the trained model
    print("Saving model...")
    model.save('trained_model.pkl')

    # Close the environment
    print("Done")
    env.close()

if __name__ == '__main__':
    #check_env(TouhouEnvironment())
    main()
