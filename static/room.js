function deleteRoom(room_id, csrf_token) {
    fetch(`deleteroom/${room_id}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
    })
      .then((data) => {
        console.log("Room deleted successfully");
        window.location.reload();
      })
      .catch((error) => console.error("Error:", error));
  }

function deleteBooking(booking_id, csrf_token) {
  fetch(`deleteBooking/${booking_id}/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
  })
    .then((data) => {
      console.log("Booking deleted successfully");
      window.location.reload();
    })
    .catch((error) => console.error("Error:", error));
}