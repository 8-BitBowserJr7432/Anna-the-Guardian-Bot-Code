require('dotenv').config();
const { Client, GatewayIntentBits, ActivityType } = require('discord.js');

// Debug log
console.log("Attempting login with token:", process.env.BOT_TOKEN ? "✔️ Present" : "❌ MISSING");

const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

client.once('ready', () => {
  console.log(`${client.user.tag} is online!`);

  client.user.setPresence({
    status: 'idle',
    activities: [{
      name: 'over the Flowers',
      type: ActivityType.Watching
    }]
  });
});

client.on('error', console.error);

client.login(process.env.BOT_TOKEN).catch(err => {
  console.error("Login failed ❌", err);
});
