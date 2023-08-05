from gym.envs.registration import register
register(
    id='haibotenv-v7', 
    entry_point='haibot_rosgymbullet.envs:DiffBotDrivingEnv'
)