//  mongosh --username my-user --password admin --authenticationDatabase knative
// use knative
db.createUser({
  user: "my-user",
  pwd: "admin",
  roles: [
    { role: "readWrite", db: "knative" },
    { role: "dbAdmin", db: "knative" },
  ],
});

db.updateUser("my-user", {
  roles: [
    { role: "readWrite", db: "knative" },
    { role: "dbAdmin", db: "knative" },
  ],
});
