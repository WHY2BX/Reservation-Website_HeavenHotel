function deletePromotion(promotion_id, csrf_token) {
    fetch(`deletepro/${promotion_id}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
    })
      .then((data) => {
        console.log("Promotion deleted successfully");
        window.location.reload();
      })
      .catch((error) => console.error("Error:", error));
  }