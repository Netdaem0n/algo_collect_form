from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TelField, SelectField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    fam_child = StringField('Фамилия ребенка', validators=[DataRequired()])
    name_child = StringField('Имя ребенка', validators=[DataRequired()])
    otch_child = StringField('Отчество ребенка', validators=[DataRequired()])
    date_birth = DateField('Дата рождения(День Месяц Год)', format='%Y-%m-%d', validators=[DataRequired()])
    name_parent = StringField('Имя родителя(законного представителя)', validators=[DataRequired()])
    phone_parent = TelField('Телефон родителя', validators=[DataRequired()])
    tg_account = StringField('Аккаунт в Telegram')
    mk_day = SelectField('День мастер-класса', validators=[DataRequired()])
    mk_time = SelectField('Время мастер-класса', validators=[DataRequired()])
    mk_name = SelectField('Мастер-класс', validators=[DataRequired()])
