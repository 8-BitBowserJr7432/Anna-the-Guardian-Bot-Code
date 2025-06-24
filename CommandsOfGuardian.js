const {
  Client,
  GatewayIntentBits,
  Events,
  PermissionsBitField,
  SlashCommandBuilder,
  REST,
  Routes
} = require('discord.js');
require('dotenv').config();

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.GuildMessages,
  ],
});

const commands = [
  new SlashCommandBuilder().setName('ping').setDescription('Replies with Pong!'),
  new SlashCommandBuilder()
    .setName('say')
    .setDescription('Replies with your input')
    .addStringOption(option =>
      option.setName('message').setDescription('Message to say').setRequired(true)),
  new SlashCommandBuilder().setName('info').setDescription('Bot info'),
  new SlashCommandBuilder()
    .setName('ban')
    .setDescription('Ban a user')
    .addUserOption(opt => opt.setName('target').setDescription('User to ban').setRequired(true))
    .addStringOption(opt => opt.setName('reason').setDescription('Reason')),
  new SlashCommandBuilder()
    .setName('kick')
    .setDescription('Kick a user')
    .addUserOption(opt => opt.setName('target').setDescription('User to kick').setRequired(true))
    .addStringOption(opt => opt.setName('reason').setDescription('Reason')),
  new SlashCommandBuilder()
    .setName('warn')
    .setDescription('Warn a user')
    .addUserOption(opt => opt.setName('target').setDescription('User to warn').setRequired(true))
    .addStringOption(opt => opt.setName('reason').setDescription('Reason')),
].map(cmd => cmd.toJSON());

client.once(Events.ClientReady, async () => {
  console.log(`🛡️ Anna-The-Guardian is online as ${client.user.tag}`);
  client.user.setStatus('online');
  client.user.setActivity('your commands', { type: 'LISTENING' });

  const rest = new REST({ version: '10' }).setToken(process.env.BOT_TOKEN);
  try {
    await rest.put(Routes.applicationCommands(client.user.id), { body: commands });
    console.log('✅ Slash commands registered');
  } catch (err) {
    console.error('❌ Registration failed:', err);
  }
});

client.on(Events.InteractionCreate, async interaction => {
  if (!interaction.isChatInputCommand()) return;

  const command = interaction.commandName;
  const admin = interaction.member.permissions.has(PermissionsBitField.Flags.Administrator);

  if (command === 'ping') {
    return interaction.reply('🏓 Pong!');
  }

  if (command === 'say') {
    return interaction.reply(interaction.options.getString('message'));
  }

  if (command === 'info') {
    return interaction.reply('🛡️ I am Anna-The-Guardian — defender of this server.');
  }

  if (['ban', 'kick', 'warn'].includes(command) && !admin) {
    return interaction.reply({ content: '❌ You need Administrator permissions.', ephemeral: true });
  }

  const target = interaction.options.getUser('target');
  const reason = interaction.options.getString('reason') || 'No reason provided';
  const member = interaction.guild.members.cache.get(target?.id);

  if (command === 'ban') {
    if (!member || !member.bannable) return interaction.reply({ content: '❌ Cannot ban this user.', ephemeral: true });
    await member.ban({ reason });
    return interaction.reply(`🔨 ${target.tag} has been banned. Reason: ${reason}`);
  }

  if (command === 'kick') {
    if (!member || !member.kickable) return interaction.reply({ content: '❌ Cannot kick this user.', ephemeral: true });
    await member.kick(reason);
    return interaction.reply(`👢 ${target.tag} has been kicked. Reason: ${reason}`);
  }

  if (command === 'warn') {
    return interaction.reply(`⚠️ ${target.tag} has been warned. Reason: ${reason}`);
  }
});

client.login(process.env.BOT_TOKEN);
