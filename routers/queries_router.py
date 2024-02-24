from fastapi import APIRouter
from database import connect


router = APIRouter(
    prefix="/queries",
    tags=["Запросы к базе данных"],
)


@router.get("/busy_employees_count")
def busy_employees_count():
    """Запрашивает из БД список сотрудников, отсортированный по количеству активных задач"""

    conn = connect()
    cur = conn.cursor()

    query = """
    SELECT e.full_name, e.job_title, COUNT(t.employee_id) AS количество_активных_задач
    FROM employees e
    LEFT JOIN tasks t ON e.id = t.employee_id AND t.status = 'В работе'
    WHERE t.employee_id IS NOT NULL
    GROUP BY e.full_name, e.job_title
    ORDER BY количество_активных_задач;
    """

    cur.execute(query)

    result = [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]
    cur.close()
    conn.close()

    return result


@router.get("/busy_employees")
def busy_employees():
    """Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач у сотрудника"""

    conn = connect()
    cur = conn.cursor()

    query = """
    SELECT employees.full_name, employees.job_title, tasks.name, tasks.description
    FROM tasks
    JOIN employees ON tasks.employee_id = employees.id
    WHERE tasks.status = 'В работе'
    ORDER BY employees.full_name DESC;
    """

    cur.execute(query)
    result = [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]
    cur.close()
    conn.close()

    return result


@router.get("/important_tasks")
def important_tasks():
    """Запрашивает из БД список важных задач не взятых в работу"""

    conn = connect()
    cur = conn.cursor()

    # Возвращает количество задач у сотрудников
    count_task_query = """
    SELECT e.full_name, COUNT(t.employee_id) 
    FROM employees e
    LEFT JOIN tasks t ON e.id = t.employee_id AND t.status = 'В работе'
    WHERE t.employee_id IS NOT NULL
    GROUP BY e.full_name, e.job_title    
    """

    cur.execute(count_task_query)
    count_task_item = cur.fetchall()
    count_task_dict = dict(count_task_item)
    min_value = min(count_task_dict.values())
    min_keys = [key for key, value in count_task_dict.items() if value == min_value]

    # Возвращает задачи и выполняющих их сотрудников
    task_emp_query = """
    select t.id, e.full_name
    from tasks t
    LEFT JOIN employees e ON t.employee_id = e.id
    where employee_id IS NOT null
    """

    cur.execute(task_emp_query)
    task_emp_query_item = cur.fetchall()
    task_emp_query_dict = dict(task_emp_query_item)

    # Возвращает задачу и ссылку на родительскую задачу
    task_dead_parent_query = """
        SELECT t.name, t.deadline, t.parent_task
        from tasks t
        where status = 'Создана' AND parent_task IS NOT null
        ORDER BY t.id
        """

    cur.execute(task_dead_parent_query)
    task_dead_parent_item = cur.fetchall()

    keys = ['important_tasks', 'deadline', 'full_name']
    values = []
    full_name_list = []
    important_tasks_list = []

    for item in task_dead_parent_item:
        values.append(item[0])
        values.append(item[1])
        parent_empl = task_emp_query_dict.get(item[2])
        empl_task_count = count_task_dict.get(parent_empl)

        if empl_task_count - min_value <= 2:
            full_name_list.append(parent_empl)
            values.append(full_name_list)
            full_name_list = []
        else:
            values.append(min_keys)

        important_dict = {key: value for key, value in zip(keys, values)}
        important_tasks_list.append(important_dict)
        values = []

    cur.close()
    conn.close()

    return important_tasks_list

@router.get("/important_tasks")
def important_tasks():
    """Запрашивает из БД список важных задач не взятых в работу"""

    conn = connect()
    cur = conn.cursor()