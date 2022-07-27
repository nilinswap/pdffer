import { hit_api } from "./utils.js";

function get_input_body(form_id) {
  const form_input = document.getElementById(form_id);
  const inputs = form_input.querySelectorAll("input");
  let input_body = {};
  for (let i = 0; i < inputs.length; i++) {
    input_body[inputs[i].name] = inputs[i].value;
  }
  return input_body;
}

export default class AuthForm {
  constructor(
    form_id,
    post_url,
    default_redirect_url,
    validate_form_func = null
  ) {
    this.form_id = form_id;
    this.default_redirect_url = default_redirect_url;
    this.validate_form_func = validate_form_func;
    this.post_url = post_url;
  }

  async registerSubmit() {
    const form_input = document.getElementById(this.form_id);
    async function hitPostApi(event) {
      
      let input_body = get_input_body(this.form_id);
      event.preventDefault();
      if (this.validate_form_func != null && !this.validate_form_func()) {
        console.log("invalid form");
        return;
      }
      const {data, status} = await hit_api(this.post_url, "POST", input_body);
      let redirect_url = this.default_redirect_url;
      if (status == 278) {
        redirect_url = data.location;
      }
      console.log("data", data);
      if (data.success) {
        console.log("success", data);
        window.location.replace(redirect_url);
      }
    }
    hitPostApi = hitPostApi.bind(this); // so that when I use 'this' inside hitPostApi, it uses 'this' as authForm object and not this in context of wherever it is being run. e.g. without this statment, 'this' will be form_input HTML Node object
    form_input.addEventListener("submit", hitPostApi);
  }
}
