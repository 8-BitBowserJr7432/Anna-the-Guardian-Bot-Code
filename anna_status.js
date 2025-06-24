const { Client, GatewayIntentBits, Events } = require('discord.js');
require('dotenv').config();

const client = new Client({
  intents: [GatewayIntentBits.Guilds],
});

client.once(Events.ClientReady, () => {
  console.log(\`🛡️ Anna-The-Guardian is online as \${client.user.tag}\`);

  // Set bot status: online | idle | dnd | invisible
  client.user.setStatus('online');

  // Set activity: PLAYING, LISTENING, WATCHING, COMPETING
  client.user.setActivity('your commands', { type: 'LISTENING' });
});

client.login(process.env.BOT_TOKEN);
