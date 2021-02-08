<template>
  <b-container fluid class="login-container">
    <img src="~/assets/img/izboljsajmo_maribor_logo.png" class="position-absolute p-4" alt="">
    <b-row class="vh-100 justify-content-center align-items-center">
      <div class="login-window">
        <Nuxt />
      </div>
    </b-row>
  </b-container>
</template>

<style lang="scss">

.login-container {
  background-image: url('~assets/img/login-background-image.png');
  background-size: cover;
  background-position: center;

  .login-window {
    background-color: #f8f8f8;
    padding: 2rem;
    border-radius: 10px;
    width: 450px;
    max-height: 80%;
    overflow-y: scroll;

    h1 {
      font-weight: 700;
      text-align: center;
      //margin-bottom: 1.5rem;
    }

    a {
      font-size: 0.75rem;
      font-style: italic;
      font-weight: 300;
      color: black;
      text-decoration: underline;

      &:hover {
        color: #ef7782;
      }
    }

    label {
      font-weight: 600;
      font-style: italic;
      font-size: 1rem;
      margin-bottom: 0.2rem;
      margin-top: 1rem;
    }

    hr {
      width: calc(450px + 4rem);
      margin-left: -2rem;
      margin-top: 0;
      margin-bottom: 1px;

      &.hr-upper {
        margin-top: 1.5rem;
        border-color: #e8e8e8;
      }

      &.hr-lower {
        margin-bottom: 1.5rem;
        border-color: white;
      }
    }

    form {
      .form-note {
        font-size: 0.75rem;
        font-style: italic;
      }

      .error-message {
        color: red;
      }

      .form-group {
        margin-bottom: 0;

        input {
          border-radius: 1.5rem;
          box-shadow: 4px 4px 6px rgba(208, 212, 220, 0.35), -4px -4px 6px #ffffff, inset 0 4px 6px rgba(208, 212, 220, 0.5);
          border: none;
        }

        input, input:focus {
          background-color: #f8f8f8;
        }
      }

      .btn {
        background-color: #ef7782;
        box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
        border-radius: 1.5rem;
        border: none;
        color: black;
        font-style: italic;
        font-weight: 700;
        letter-spacing: 0.1rem;
        margin: 1rem 0;
      }
    }
  }
}

.custom-radio {
  label.custom-control-label {
    &:before, &:after {
      top: -0.1rem;
      left: -2rem;
      width: 1.5rem;
      height: 1.5rem;
    }
  }

  .custom-control-input:checked ~ .custom-control-label {
    &:before {
      background-color: #ef7782;
      border-color: #ef7782;
    }

    &:after {
      background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 8 8'%3e%3cpath fill='%23fff' d='M6.564.75l-3.59 3.612-1.538-1.55L0 4.26l2.974 2.99L8 2.193z'/%3e%3c/svg%3e");
    }
  }
}

.custom-checkbox {
  padding-left: 2rem;
  margin-bottom: 1rem;

  .custom-control-input:checked ~ .custom-control-label {
    &:after {
      background-color: #ef7782;
    }
  }

  label.custom-control-label {
    font-weight: normal;
    font-size: 0.75rem;

    &:before, &:after {
      top: -0.1rem;
      left: -2rem;
      width: 1.5rem;
      height: 1.5rem;
      box-shadow: 3px 3px 4px rgba(208, 212, 220, 0.35), -3px -3px 4px #ffffff, inset 0 3px 4px rgba(208, 212, 220, 0.5);
      border: none;
      border-radius: 3px;
    }

    &:before {
      background-color: #f8f8f8;
    }
  }
}

</style>
