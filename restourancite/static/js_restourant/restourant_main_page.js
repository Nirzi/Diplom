document.getElementById('button_submit_bron').addEventListener('click', function(event) {
  event.preventDefault(); // Остановить стандартное поведение кнопки отправки формы

  const form_name = document.getElementById('form_name').value.trim();
  const form_surname = document.getElementById('form_surname').value.trim();
  const form_telephone = document.getElementById('form_telephone').value.trim();
  const form_date = document.getElementById('form_date').value;
  const form_time = document.getElementById('form_time').value;
  const flexCheckDefault = document.getElementById('flexCheckDefault');
  const form_number_guest = document.getElementById('form_number_guest').value.trim();

  // Проверки перед отправкой формы
  if (form_name === '') {
      alert('Пожалуйста, введите своё имя');
      return; // Выход из функции
  } 
  if (form_surname === '') {
      alert('Пожалуйста, введите свою фамилию');
      return; // Выход из функции
  } 
  if (form_telephone === '') {
      alert('Пожалуйста, введите свой номер телефона');
      return; // Выход из функции
  } 
  if (form_date === '') {
      alert('Пожалуйста, введите дату записи');
      return; // Выход из функции
  } 
  if (form_time === '') {
      alert('Пожалуйста, введите время записи');
      return; // Выход из функции
  } 
  if (form_number_guest === '') {
      alert('Пожалуйста, введите количество гостей');
      return; // Выход из функции
  } 
  if (!flexCheckDefault.checked) {
      alert('Пожалуйста, подтвердите своё согласие на обработку персональных данных');
      return; // Выход из функции
  } 

  // Проверка на валидность даты
  const selectedDate = new Date(form_date);
  const currentDate = new Date();
  currentDate.setHours(0, 0, 0, 0); // Установите время на полночь для корректного сравнения
  const maxDate = new Date('2027-12-31'); // Максимальная дата - 31 декабря 2027 года

  // Проверка: дата не должна быть меньше текущей и не больше 2027 года
  if (selectedDate < currentDate) {
      alert('Дата не может быть меньше текущей даты');
      return; // Выход из функции
  } 
  if (selectedDate > maxDate) {
      alert('Дата не может быть больше 31 декабря 2027 года');
      return; // Выход из функции
  } 

  // Если все проверки пройдены, отправляем форму
  document.getElementById('form_bron_table').submit(); // Отправка формы на сервер
});




