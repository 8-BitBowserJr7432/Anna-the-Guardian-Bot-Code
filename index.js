client.once("ready", () => {
  console.log(`✅ Anna the Guardian is online as ${client.user.tag}`);
  client.user.setPresence({
    status: "dnd", // online, idle, dnd, invisible
    activities: [
      {
        name: "Some cool flowers",
        type: 3 // Watching
      }
    ]
  });
});

// Login process
client.login(process.env.DISCORD_TOKEN);
