//funcao que valda cpf
function isValidCPF(cpf) {
  cpf = cpf.replace(/\D/g, '');
  if (cpf.length !== 11) {
    return false;
  }

  if (/^(\d)\1{10}$/.test(cpf)) {
    return false;
  }

  let sum = 0;
  for (let i = 0; i < 9; i++) {
    sum += parseInt(cpf.charAt(i)) * (10 - i);
  }
  let remainder = sum % 11;
  let digit1 = remainder < 2 ? 0 : 11 - remainder;

  sum = 0;
  for (let i = 0; i < 10; i++) {
    sum += parseInt(cpf.charAt(i)) * (11 - i);
  }
  remainder = sum % 11;
  let digit2 = remainder < 2 ? 0 : 11 - remainder;
  return (
    parseInt(cpf.charAt(9)) === digit1 && parseInt(cpf.charAt(10)) === digit2
  );
}

// funcao que valida CNPJ
function isValidCNPJ(cnpj) {
  cnpj = cnpj.replace(/\D/g, '');

  if (cnpj.length !== 14) {
    return false;
  }

  let sum = 0;
  let multiplier = 5;
  for (let i = 0; i < 12; i++) {
    sum += parseInt(cnpj.charAt(i)) * multiplier;
    multiplier = multiplier === 2 ? 9 : multiplier - 1;
  }
  let remainder = sum % 11;
  let digit1 = remainder < 2 ? 0 : 11 - remainder;

  sum = 0;
  multiplier = 6;
  for (let i = 0; i < 13; i++) {
    sum += parseInt(cnpj.charAt(i)) * multiplier;
    multiplier = multiplier === 2 ? 9 : multiplier - 1;
  }
  remainder = sum % 11;
  let digit2 = remainder < 2 ? 0 : 11 - remainder;

  return (
    parseInt(cnpj.charAt(12)) === digit1 && parseInt(cnpj.charAt(13)) === digit2
  );
}

//funcao que valida CEP
function isValidCEP(cep) {
  var cepPattern = /^\d{5}-\d{3}$/;
  return cepPattern.test(cep);
}

function openModal() {
  new bootstrap.Modal('#exampleModal').show();
}

function openModal(clientId) {
  // Send AJAX request to fetch client information
  fetch(`/view_client/${clientId}`)
    .then((response) => response.json())
    .then((data) => {
      // Populate form fields with client information
      document.getElementById('client_id').value = data.client_id;
      document.getElementById('clientName').value = data.clientName;
      document.getElementById('cpf').value = data.cpf;
      document.getElementById('RazaoSocial').value = data.RazaoSocial;
      document.getElementById('cnpj').value = data.cnpj;
      document.getElementById('Telephone').value = data.Telephone;
      document.getElementById('Cellphone').value = data.Cellphone;
      document.getElementById('Email1').value = data.Email1;
      document.getElementById('Email2').value = data.Email2;
      document.getElementById('CEP').value = data.CEP;
      document.getElementById('Logradouro').value = data.Logradouro;
      document.getElementById('Numero').value = data.Numero;
      document.getElementById('Complemento').value = data.Complemento;
      document.getElementById('brazilianStates').value = data.brazilianStates;
      document.getElementById('city').value = data.city;

      // Show the modal
      const modal = new bootstrap.Modal(
        document.getElementById('exampleModalCliente')
      );
      modal.show();
    })
    .catch((error) => console.error('Error:', error));
}

function openModalVeiculo(veiculoId) {
  // Send AJAX request to fetch client information
  fetch(`/view_veiculo/${veiculoId}`)
    .then((response) => response.json())
    .then((data) => {
      // Populate form fields with client information
      document.getElementById('id').value = data.id;
      document.getElementById('placa').value = data.placa;
      document.getElementById('cpf').value = data.cpf;
      document.getElementById('cnpj').value = data.cnpj;
      document.getElementById('chassi').value = data.chassi;
      document.getElementById('fabricante').value = data.fabricante;
      document.getElementById('modelo').value = data.modelo;
      document.getElementById('cor').value = data.cor;
      document.getElementById('ano_modelo').value = data.ano_modelo;
      document.getElementById('client_id').value = data.client_id;

      // Show the modal
      const modal = new bootstrap.Modal(
        document.getElementById('exampleModalCliente')
      );
      modal.show();
    })
    .catch((error) => console.error('Error:', error));
}

function openModal1() {
  console.log('openModal1 function called');
  var clientName = $('#clientName').val(); // Get the value of the clientName input
  var modal = new bootstrap.Modal(document.getElementById('exampleModal1'));
  var clientNameMessage = document.getElementById('clientNameMessage');

  // Update modal content based on clientName
  clientNameMessage.textContent = clientName + ' cadastrado(a) com Sucesso';

  // Show the modal
  modal.show();
  console.log('Modal shown');
}

$(document).ready(function () {
  $('#openModalButton').click(function () {
    openModal1();
  });
});

function openModal3() {
  console.log('openModal3 function called');
  var placa = $('#placa').val(); // Get the value of the clientName input
  var modal = new bootstrap.Modal(document.getElementById('exampleModal3'));
  var placaMessage = document.getElementById('placaMessage');

  // Update modal content based on clientName
  placaMessage.textContent = placa + ' cadastrado(a) com Sucesso';

  // Show the modal
  modal.show();
  console.log('Modal shown');
}

$(document).ready(function () {
  $('#openModalButton3').click(function () {
    openModal3();
  });
});

function cadastrarVeiculo() {
  var client_id = $('#client_id_input').val(); // Retrieve the client_id from the hidden input field

  // Form data for vehicle registration
  var formData = $('#clientVehicleForm').serialize();

  // Add the client_id to the formData
  formData += '&client_id=' + client_id;

  // Perform an AJAX request to register the vehicle
  $.ajax({
    url: '/vehicle_registration', // Update with the correct endpoint
    method: 'POST',
    data: formData,
    success: function (response) {
      // Handle success response, if needed
      console.log('Vehicle registration successful.');
    },
    error: function (xhr, status, error) {
      // Handle error response, if needed
      console.error('Error registering vehicle:', error);
    },
  });
}

$(document).ready(function () {
  $('#openRegistroVeiculo').click(function () {
    cadastrarVeiculo();
  });
});

$(document).ready(function () {
  // When the page is loaded
  var urlParams = new URLSearchParams(window.location.search);
  var clientId = urlParams.get('client_id');

  // Set the value of the input field to the client ID
  $('#client_id').val(clientId);
});

$(document).ready(function () {
  // When the page is loaded
  var urlParams = new URLSearchParams(window.location.search);
  var placa = urlParams.get('placa');

  // Set the value of the input field to the client ID
  $('#placa').val(placa);
});

$(document).ready(function () {
  // Bind click event handler to the button with id 'redirecionaToVehicleRegistration'
  $('#redirecionaToVehicleRegistration').click(function () {
    // Redirect to the vehicle_registration page
    window.location.href = '/vehicle_registration';
  });
});

$(document).ready(function () {
  // Bind click event handler to the button with id 'redirecionaToVehicleRegistration'
  $('#redirecionaOrdem').click(function () {
    // Redirect to the vehicle_registration page
    window.location.href = '/order';
  });
});

// Function to search for a client
function searchClient() {
  const cpfCnpj = document.getElementById('cpfCnpj').value;

  // Send a request to the backend to search for the client
  $.ajax({
    url: '/search_client',
    method: 'POST', // Change method to POST
    data: { cpfCnpj: cpfCnpj },
    success: function (response) {
      // Display the retrieved client information
      displayClientInfo(response);
    },
    error: function (xhr, status, error) {
      console.error('Failed to search for client:', error);
    },
  });
}

// Function to display client information
function displayClientInfo(clientData) {
  const clientInfo = document.getElementById('clientInfo');
  const clientNameSpan = document.getElementById('clientName');
  const clientCpfCnpjSpan = document.getElementById('clientCpfCnpj');
  const vehicleSelect = document.getElementById('vehicleSelect');
  const mechanicalServicesSelect =
    document.getElementById('mechanicalServices');

  clientNameSpan.textContent = clientData.name;
  clientCpfCnpjSpan.textContent = clientData.cpfCnpj;

  // Populate the vehicle dropdown
  clientData.vehicles.forEach((vehicle) => {
    const option = document.createElement('option');
    option.value = vehicle.numberPlate;
    option.textContent = vehicle.numberPlate;
    vehicleSelect.appendChild(option);
  });

  // Populate the mechanical services dropdown
  clientData.services.forEach((service) => {
    const option = document.createElement('option');
    option.value = service.id;
    option.textContent = service.nome;
    mechanicalServicesSelect.appendChild(option);
  });

  // Show the client info section
  clientInfo.style.display = 'block';
}

// Function to load service prices based on the selected services
function loadServices() {
  const selectedServices = Array.from(
    document.getElementById('mechanicalServices').selectedOptions
  ).map((option) => option.value);

  // Send a request to the backend to get service prices
  $.ajax({
    url: '/get_service_prices',
    method: 'POST',
    data: { services: selectedServices },
    success: function (response) {
      // Display service prices
      displayServicePrices(response);
    },
    error: function (xhr, status, error) {
      console.error('Failed to retrieve service prices:', error);
    },
  });
}

// Function to display service prices
function displayServicePrices(servicePricesData) {
  const servicePricesDiv = document.getElementById('servicePrices');

  // Clear previous prices
  servicePricesDiv.innerHTML = '';

  // Display prices for selected services
  for (const serviceId in servicePricesData) {
    const priceParagraph = document.createElement('p');
    priceParagraph.textContent = `${serviceId}: $${servicePricesData[serviceId]}`;
    servicePricesDiv.appendChild(priceParagraph);
  }
}

// Function to simulate printing and sharing
function printAndShare() {
  // You can implement actual print and share functionality here
  alert('Printing and Sharing...');
}

///---------------> STATUS PAGES <--------------------------

// Add event listener for dragstart to add dragging class
document.addEventListener('dragstart', function (e) {
  e.target.classList.add('dragging');
});

// Add event listener for dragover to allow drop
document.addEventListener('dragover', function (e) {
  e.preventDefault();
});

// Add event listener for drop to handle movement between containers
document.addEventListener('drop', function (e) {
  e.preventDefault();
  const draggedElement = document.querySelector('.list.dragging');
  if (draggedElement) {
    const dropZone = e.target.closest('#left, #right, #last');
    if (dropZone) {
      if (dropZone.id === 'left') {
        // Move to the left container
        document.getElementById('left').appendChild(draggedElement);
      } else if (dropZone.id === 'right') {
        // Move to the right container
        document.getElementById('right').appendChild(draggedElement);
      } else if (dropZone.id === 'last') {
        // Move to the right container
        document.getElementById('last').appendChild(draggedElement);
      }

      // Remove the dragging class after drop
      draggedElement.classList.remove('dragging');
    }
  }
});

document
  .getElementById('redirecionaOrdem')
  .addEventListener('click', function () {
    // Redirect to the abrirordem page with client_id and veiculo_id parameters
    var client_id = 1; // Replace with actual client_id
    var veiculo_id = 1; // Replace with actual veiculo_id
    window.location.href =
      "{{ url_for('show_ordem') }}?client_id=" +
      client_id +
      '&veiculo_id=' +
      veiculo_id;
  });

// Calculate subtotal based on selected services
document.getElementById('tipo_servico').addEventListener('change', function () {
  // Get selected option
  let selectedOption = this.options[this.selectedIndex];
  // Extract valor from option value
  let valor = parseFloat(selectedOption.value.split(' ')[1].substring(2));
  // Update subtotal field with the selected service valor
  document.getElementById('subtotal').textContent = `R$ ${valor.toFixed(2)}`;
});
