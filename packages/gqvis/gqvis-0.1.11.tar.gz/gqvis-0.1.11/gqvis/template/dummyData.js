dummyData = {
  nodes: [
    {
      id: 1,
      category: "Item",
      name: "Item",
    },
    {
      id: 2,
      category: "Consumable",
      name: "Consumable",
    },
    {
      id: 3,
      category: "Activity",
      name: "Activity/Activity",
    },
    {
      id: 4,
      category: "Activity",
      name: "Activity/Inspect",
    },
    {
      id: 5,
      category: "Activity",
      name: "Activity/Minor_Maintenance",
    },
  ],
  links: [
    {
      source: 1,
      target: 2,
      type: "REL_1",
    },
    {
      source: 2,
      target: 3,
      type: "REL_1",
    },
    {
      source: 1,
      target: 3,
      type: "REL_2",
    },
    {
      source: 4,
      target: 5,
      type: "REL_2",
    },
  ],
};
