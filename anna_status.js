const { Client, GatewayIntentBits, Events } = require('discord.js');
require('dotenv').config();

const client = new Client({
  intents: [GatewayIntentBits.Guilds],
});

client.once(Events.ClientReady, () => {
  console.log(\`Anna-The-Guardian is online as \${client.user.tag}\`);

  // Set bot status: online | idle | dnd | invisible
  client.user.setStatus('idle');

  // Set activity: PLAYING, LISTENING, WATCHING, COMPETING
  client.user.setActivity('Codded By Luis', { type: 'COMPETTING' });
});

client.login(process.env.BOT_TOKEN);
