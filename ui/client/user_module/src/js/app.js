"use strict";

import axios from "axios";

(async function () {
  async function fetchData() {
    try {
      const response = await axios.get("/api");
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  // Call the function
  await fetchData();
})();
