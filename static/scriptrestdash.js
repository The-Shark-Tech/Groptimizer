let inventory = [
    { name: "Rice", quantity: 200 },
    { name: "Beans", quantity: 100 },
    { name: "Canned Vegetables", quantity: 300 },
];

function renderInventory() {
    const tbody = document.querySelector("#restaurant-table tbody");
    tbody.innerHTML = "";

    inventory.forEach((item, index) => {
        const row = `
            <tr>
                <td>${item.name}</td>
                <td><input type="number" value="${item.quantity}" min="0" onchange="updateQuantity(${index}, this.value)"></td>
                <td><button onclick="removeItem (${index})">Remove</button></td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function addItem() {
    const name = prompt("Enter item name:");
    if (name) {
        const quantity = prompt("Enter quantity:");
        if (quantity) {
            const newItem = { name, quantity: parseInt(quantity) };
            inventory.push(newItem);
            renderInventory();
        }
    }
}

function updateQuantity(index, newQuantity) {
    inventory[index].quantity = parseInt(newQuantity);
}

function removeItem(index) {
    inventory.splice(index, 1);
    renderInventory();
}
function sendAlert() {
    const message = document.getElementById("alertMessage").value;
    window.alert("Alert sent to Food Banks: " + message);
    // Clear the message box after sending the alert
    document.getElementById("alertMessage").value = "";
}
renderInventory();
