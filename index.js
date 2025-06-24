require('dotenv').config(); // Load .env variables
const { Client, GatewayIntentBits, ActivityType } = require('discord.js');

// Check if token exists
if (!process.env.BOT_TOKEN) {
  console.error('❌ BOT_TOKEN is missing in your .env file');
  process.exit(1);
}

const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

client.once('ready', () => {
  console.log(`✅ ${client.user.tag} is online!`);

  client.user.setPresence({
    status: 'idle',
    activities: [
      {
        name: 'over the flowers',
        type: ActivityType.Watching
      }
    ]
  });
});

// Login with token
client.login(process.env.BOT_TOKEN).catch((err) => {
  console.error('❌ Login failed:', err);
});
