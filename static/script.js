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
  fetch(`/view/${clientId}`)
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
        document.getElementById('exampleModal')
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
  var clientName = $('#placa').val(); // Get the value of the clientName input
  var modal = new bootstrap.Modal(document.getElementById('exampleModal3'));
  var clientNameMessage = document.getElementById('placaMessage');

  // Update modal content based on clientName
  clientNameMessage.textContent = placa + ' cadastrado(a) com Sucesso';

  // Show the modal
  modal.show();
  console.log('Modal shown');
}

$(document).ready(function () {
  $('#openModalButton3').click(function () {
    openModal3();
  });
});

function cadastrarVeiculo(last_client_id) {
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
