from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database import SessionLocal
from auth import authenticate_user
import streamlit.components.v1 as components
from datetime import UTC, datetime
from datetime import date
import calendar
from models import User
from decimal import Decimal
from sqlalchemy import func, select
from werkzeug.security import check_password_hash, generate_password_hash
from models import (
    FinancialTransaction,
    JournalEntry,
    Task,
)

st.set_page_config(
    page_title="Personal Productivity",
    page_icon="📋",
    layout="wide",
)


# ============================================================
# Login
# ============================================================

def login_page():
    st.title("Personal Productivity")
    st.subheader("Sign in to your account")

    with st.form("login_form"):
        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True,
        )

    if not submitted:
        return

    if not username or not password:
        st.error("Please enter your username and password.")
        return

    session = SessionLocal()

    try:
        user = authenticate_user(
            session,
            username,
            password,
        )

        if user is None:
            st.error("Invalid username or password.")
            return

        st.session_state["logged_in"] = True
        st.session_state["user_id"] = user.id
        st.session_state["username"] = user.username
        st.session_state["full_name"] = user.full_name

    finally:
        session.close()

    st.rerun()


# ============================================================
# Sidebar
# ============================================================

def sidebar():
    with st.sidebar:
        st.title("📋 Personal Productivity")

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "✅ Tasks",
                "💰 Finance",
                "📔 Journal",
                "⚙️ Settings",
            ],
        )

        st.divider()

        st.caption(
            f"User: {st.session_state.get('full_name', '')}"
        )

        if st.button(
            "🚪 Sign Out",
            use_container_width=True,
        ):
            st.session_state.clear()
            st.rerun()

    return page

# ============================================================
# Luxury Clock
# ============================================================

def luxury_clock():
    clock_html = """
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            background: transparent;
            font-family: Arial, sans-serif;
        }

        .clock-wrapper {
            width: 330px;
            height: 330px;
            margin: 0 auto;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .clock {
            position: relative;
            width: 300px;
            height: 300px;
            border-radius: 50%;

            background:
                radial-gradient(
                    circle at center,
                    #17191d 0%,
                    #0d0f12 65%,
                    #07080a 100%
                );

            border: 4px solid #8d6a32;

            box-shadow:
                0 0 0 3px #24262a,
                0 0 0 6px #b18a48,
                0 15px 35px rgba(0, 0, 0, 0.65),
                inset 0 0 25px rgba(255, 255, 255, 0.04);
        }

        .inner-ring {
            position: absolute;
            inset: 12px;
            border-radius: 50%;
            border: 1px solid #55401f;
            box-shadow:
                inset 0 0 12px rgba(255, 255, 255, 0.04);
        }

        .brand {
            position: absolute;
            top: 73px;
            left: 0;
            right: 0;
            text-align: center;
            color: #d8b36a;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 2px;
        }

        .crown {
            position: absolute;
            top: 45px;
            left: 0;
            right: 0;
            text-align: center;
            color: #d8b36a;
            font-size: 24px;
        }

        .number {
            position: absolute;
            color: #e0bd7a;
            font-family: Georgia, serif;
            font-size: 31px;
            font-weight: bold;
            text-shadow: 0 1px 4px #000;
        }

        .n12 {
            top: 25px;
            left: 50%;
            transform: translateX(-50%);
        }

        .n3 {
            right: 29px;
            top: 50%;
            transform: translateY(-50%);
        }

        .n6 {
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
        }

        .n9 {
            left: 29px;
            top: 50%;
            transform: translateY(-50%);
        }

        

    

        .tick {
            position: absolute;
            width: 2px;
            height: 8px;
            background: #9d7b43;
            left: 50%;
            top: 50%;
            transform-origin: 50% 115px;
        }

     .tick.t1 { transform: translate(-50%, -115px) rotate(30deg); }
     .tick.t2 { transform: translate(-50%, -115px) rotate(60deg); }
     .tick.t3 { transform: translate(-50%, -115px) rotate(120deg); }
     .tick.t4 { transform: translate(-50%, -115px) rotate(150deg); }
     .tick.t5 { transform: translate(-50%, -115px) rotate(210deg); }
     .tick.t6 { transform: translate(-50%, -115px) rotate(240deg); }
     .tick.t7 { transform: translate(-50%, -115px) rotate(300deg); }
     .tick.t8 { transform: translate(-50%, -115px) rotate(330deg); }

        .hand {
            position: absolute;
            left: 50%;
            bottom: 50%;
            transform-origin: 50% 100%;
            border-radius: 5px;
            z-index: 10;
        }

        .hour-hand {
            width: 7px;
            height: 76px;
            background: linear-gradient(
                to right,
                #9a712f,
                #f0cf87,
                #9a712f
            );
        }

        .minute-hand {
            width: 5px;
            height: 105px;
            background: linear-gradient(
                to right,
                #9a712f,
                #f6d995,
                #9a712f
            );
        }

        .second-hand {
            width: 2px;
            height: 116px;
            background: #d6a84f;
            z-index: 11;
        }

        .center {
            position: absolute;
            width: 17px;
            height: 17px;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            background: #d2a858;
            border: 3px solid #2a2114;
            z-index: 20;
            box-shadow: 0 0 5px rgba(212, 168, 88, 0.7);
        }

        .date-display {
            position: absolute;
            left: 50%;
            bottom: 59px;
            transform: translateX(-50%);

            min-width: 125px;
            padding: 5px 10px;

            text-align: center;

            color: #e2bd76;
            background: #0a0b0d;

            border: 1px solid #765523;
            border-radius: 4px;

            font-family: Georgia, serif;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 1px;

            box-shadow:
                inset 0 0 8px rgba(255, 255, 255, 0.03),
                0 2px 5px rgba(0, 0, 0, 0.5);

            z-index: 5;
        }

        .day-display {
            position: absolute;
            left: 50%;
            bottom: 89px;
            transform: translateX(-50%);

            color: #e2bd76;
            font-family: Georgia, serif;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 1.5px;

            z-index: 5;
        }
    </style>

    <div class="clock-wrapper">
        <div class="clock">

            <div class="inner-ring"></div>

            <div class="crown">♛</div>

            <div class="brand">
                PERSONAL<br>
                PRODUCTIVITY
            </div>

            <div class="number n12">12</div>
            <div class="number n3">3</div>
            <div class="number n6">6</div>
            <div class="number n9">9</div>

            <div class="tick t1"></div>
            <div class="tick t2"></div>
            <div class="tick t3"></div>
            <div class="tick t4"></div>
            <div class="tick t5"></div>
            <div class="tick t6"></div>
            <div class="tick t7"></div>
            <div class="tick t8"></div>

            <div class="hand hour-hand" id="hour"></div>
            <div class="hand minute-hand" id="minute"></div>
            <div class="hand second-hand" id="second"></div>

            <div class="center"></div>

            <div class="day-display" id="day"></div>
            <div class="date-display" id="date"></div>

        </div>
    </div>

    <script>
        function updateClock() {
            const now = new Date();

            const hours = now.getHours();
            const minutes = now.getMinutes();
            const seconds = now.getSeconds();

            const hourAngle =
                (hours % 12) * 30 +
                minutes * 0.5;

            const minuteAngle =
                minutes * 6 +
                seconds * 0.1;

            const secondAngle =
                seconds * 6;

            document.getElementById("hour").style.transform =
                `translateX(-50%) rotate(${hourAngle}deg)`;

            document.getElementById("minute").style.transform =
                `translateX(-50%) rotate(${minuteAngle}deg)`;

            document.getElementById("second").style.transform =
                `translateX(-50%) rotate(${secondAngle}deg)`;

            const days = [
                "SUNDAY",
                "MONDAY",
                "TUESDAY",
                "WEDNESDAY",
                "THURSDAY",
                "FRIDAY",
                "SATURDAY"
            ];

            const months = [
                "JAN",
                "FEB",
                "MAR",
                "APR",
                "MAY",
                "JUN",
                "JUL",
                "AUG",
                "SEP",
                "OCT",
                "NOV",
                "DEC"
            ];

            document.getElementById("day").textContent =
                days[now.getDay()];

            document.getElementById("date").textContent =
                `${now.getDate()} ${months[now.getMonth()]} ${now.getFullYear()}`;
        }

        updateClock();

        setInterval(updateClock, 1000);
    </script>
    """

    components.html(
        clock_html,
        height=350,
    )

# ============================================================
# Dashboard
# ============================================================

def dashboard_page():
    user_id = st.session_state["user_id"]

    full_name = st.session_state.get(
        "full_name",
        st.session_state.get("username", ""),
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.title(f"Hello, {full_name} 👋")
        st.caption("Here is your productivity overview.")

    with col2:
        luxury_clock()

    session = SessionLocal()

    try:
        today = date.today()

        # ========================================================
        # Task Statistics
        # ========================================================

        today_tasks = session.scalar(
            select(func.count(Task.id))
            .where(
                Task.user_id == user_id,
                Task.due_date == today,
            )
        ) or 0

        pending_tasks = session.scalar(
            select(func.count(Task.id))
            .where(
                Task.user_id == user_id,
                Task.status == "pending",
            )
        ) or 0

        completed_tasks = session.scalar(
            select(func.count(Task.id))
            .where(
                Task.user_id == user_id,
                Task.status == "completed",
            )
        ) or 0

        # ========================================================
        # Finance Statistics
        # ========================================================

        total_income = session.scalar(
            select(
                func.coalesce(
                    func.sum(
                        FinancialTransaction.amount
                    ),
                    0,
                )
            )
            .where(
                FinancialTransaction.user_id == user_id,
                FinancialTransaction.transaction_type
                == "income",
            )
        )

        total_expense = session.scalar(
            select(
                func.coalesce(
                    func.sum(
                        FinancialTransaction.amount
                    ),
                    0,
                )
            )
            .where(
                FinancialTransaction.user_id == user_id,
                FinancialTransaction.transaction_type
                == "expense",
            )
        )

        total_income = Decimal(str(total_income))
        total_expense = Decimal(str(total_expense))

        balance = total_income - total_expense

        # ========================================================
        # Journal Statistics
        # ========================================================

        today_journal_entries = session.scalar(
            select(func.count(JournalEntry.id))
            .where(
                JournalEntry.user_id == user_id,
                JournalEntry.entry_date == today,
            )
        ) or 0

        total_journal_entries = session.scalar(
            select(func.count(JournalEntry.id))
            .where(
                JournalEntry.user_id == user_id,
            )
        ) or 0

        # ========================================================
        # Main Metrics
        # ========================================================

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Today's Tasks",
                today_tasks,
            )

        with col2:
            st.metric(
                "Pending Tasks",
                pending_tasks,
            )

        with col3:
            st.metric(
                "Current Balance",
                f"{balance:,.0f} Toman",
            )

        with col4:
            st.metric(
                "Today's Journal",
                today_journal_entries,
            )

        # ========================================================
        # Productivity Overview
        # ========================================================

        st.divider()

        st.subheader("Productivity Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Tasks")

            task_col1, task_col2 = st.columns(2)

            with task_col1:
                st.metric(
                    "Pending",
                    pending_tasks,
                )

            with task_col2:
                st.metric(
                    "Completed",
                    completed_tasks,
                )

        with col2:
            st.markdown("### 💰 Finance")

            finance_col1, finance_col2 = st.columns(2)

            with finance_col1:
                st.metric(
                    "Income",
                    f"{total_income:,.0f}",
                )

            with finance_col2:
                st.metric(
                    "Expense",
                    f"{total_expense:,.0f}",
                )

        # ========================================================
        # Journal Overview
        # ========================================================

        st.divider()

        st.subheader("📔 Journal")

        st.metric(
            "Total Journal Entries",
            total_journal_entries,
        )

        # ========================================================
        # Recent Tasks
        # ========================================================

        st.divider()

        st.subheader("📋 Recent Tasks")

        recent_tasks = session.scalars(
            select(Task)
            .where(
                Task.user_id == user_id,
            )
            .order_by(
                Task.created_at.desc()
            )
            .limit(5)
        ).all()

        if not recent_tasks:
            st.info("No tasks found.")

        else:
            for task in recent_tasks:

                status_icon = (
                    "✅"
                    if task.status == "completed"
                    else "⏳"
                )

                st.write(
                    f"{status_icon} **{task.title}**"
                )

        # ========================================================
        # Recent Journal Entries
        # ========================================================

        st.divider()

        st.subheader("📔 Recent Journal Entries")

        recent_entries = session.scalars(
            select(JournalEntry)
            .where(
                JournalEntry.user_id == user_id,
            )
            .order_by(
                JournalEntry.created_at.desc()
            )
            .limit(3)
        ).all()

        if not recent_entries:
            st.info("No journal entries found.")

        else:
            for entry in recent_entries:

                title = (
                    entry.title
                    if entry.title
                    else "Untitled Entry"
                )

                st.write(
                    f"📔 **{title}** — "
                    f"{entry.entry_date}"
                )

    finally:
        session.close()


# ============================================================
# Tasks
# ============================================================

# ============================================================
# Tasks
# ============================================================

def tasks_page():
    st.title("✅ Tasks")

    user_id = st.session_state["user_id"]

    # --------------------------------------------------------
    # Add Task
    # --------------------------------------------------------

    with st.expander("➕ Add New Task", expanded=True):
        with st.form("add_task_form"):
            title = st.text_input("Title")

            description = st.text_area(
                "Description",
            )

            col1, col2 = st.columns(2)

            with col1:
                priority = st.selectbox(
                    "Priority",
                    [
                        "low",
                        "normal",
                        "high",
                    ],
                    index=1,
                )

            with col2:
                due_date = st.date_input(
                    "Due Date",
                    value=None,
                )

            submitted = st.form_submit_button(
                "Add Task",
                use_container_width=True,
            )

        if submitted:
            if not title.strip():
                st.error("Task title cannot be empty.")
            else:
                session = SessionLocal()

                try:
                    new_task = Task(
                        user_id=user_id,
                        title=title.strip(),
                        description=description.strip() or None,
                        status="pending",
                        priority=priority,
                        due_date=due_date,
                        created_at=datetime.now(UTC),
                    )

                    session.add(new_task)
                    session.commit()

                    st.success("Task added successfully.")
                    st.rerun()


                except SQLAlchemyError:
                    session.rollback()
                    st.error("Failed to add task.")

                finally:
                    session.close()

    st.divider()

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    st.subheader("Your Tasks")

    col1, col2 = st.columns(2)

    with col1:
        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Pending",
                "Completed",
            ],
        )

    with col2:
        priority_filter = st.selectbox(
            "Priority",
            [
                "All",
                "Low",
                "Normal",
                "High",
            ],
        )

    # --------------------------------------------------------
    # Load Tasks
    # --------------------------------------------------------

    session = SessionLocal()

    try:
        query = select(Task).where(
            Task.user_id == user_id
        )

        if status_filter == "Pending":
            query = query.where(
                Task.status == "pending"
            )

        elif status_filter == "Completed":
            query = query.where(
                Task.status == "completed"
            )

        if priority_filter != "All":
            query = query.where(
                Task.priority == priority_filter.lower()
            )

        query = query.order_by(
            Task.created_at.desc()
        )

        tasks = session.scalars(query).all()

    finally:
        session.close()

    # --------------------------------------------------------
    # Task Statistics
    # --------------------------------------------------------

    total_tasks = len(tasks)

    pending_tasks = sum(
        1
        for task in tasks
        if task.status == "pending"
    )

    completed_tasks = sum(
        1
        for task in tasks
        if task.status == "completed"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total",
            total_tasks,
        )

    with col2:
        st.metric(
            "Pending",
            pending_tasks,
        )

    with col3:
        st.metric(
            "Completed",
            completed_tasks,
        )

    st.divider()

    # --------------------------------------------------------
    # Display Tasks
    # --------------------------------------------------------

    if not tasks:
        st.info("No tasks found.")
        return

    for task in tasks:

        status_icon = (
            "✅"
            if task.status == "completed"
            else "⏳"
        )

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [5, 2, 1]
            )

            with col1:
                st.subheader(
                    f"{status_icon} {task.title}"
                )

                if task.description:
                    st.write(task.description)

                if task.due_date:
                    st.caption(
                        f"Due date: {task.due_date}"
                    )

            with col2:
                st.write(
                    f"Priority: **{task.priority.title()}**"
                )

                st.write(
                    f"Status: **{task.status.title()}**"
                )

            with col3:
                if task.status == "pending":

                    if st.button(
                        "Complete",
                        key=f"complete_{task.id}",
                        use_container_width=True,
                    ):
                        session = SessionLocal()

                        try:
                            db_task = session.get(
                                Task,
                                task.id,
                            )

                            if (
                                db_task
                                and db_task.user_id == user_id
                            ):
                                db_task.status = "completed"
                                db_task.completed_at = datetime.now(UTC)

                                session.commit()

                        finally:
                            session.close()

                        st.rerun()

                else:

                    if st.button(
                        "Reopen",
                        key=f"reopen_{task.id}",
                        use_container_width=True,
                    ):
                        session = SessionLocal()

                        try:
                            db_task = session.get(
                                Task,
                                task.id,
                            )

                            if (
                                db_task
                                and db_task.user_id == user_id
                            ):
                                db_task.status = "pending"
                                db_task.completed_at = None

                                session.commit()

                        finally:
                            session.close()

                        st.rerun()

            col1, col2 = st.columns(2)

            with col1:

                with st.popover("✏️ Edit"):
                    edit_title = st.text_input(
                        "Title",
                        value=task.title,
                        key=f"title_{task.id}",
                    )

                    edit_description = st.text_area(
                        "Description",
                        value=task.description or "",
                        key=f"description_{task.id}",
                    )

                    edit_priority = st.selectbox(
                        "Priority",
                        [
                            "low",
                            "normal",
                            "high",
                        ],
                        index=[
                            "low",
                            "normal",
                            "high",
                        ].index(task.priority),
                        key=f"priority_{task.id}",
                    )

                    edit_due_date = st.date_input(
                        "Due Date",
                        value=task.due_date,
                        key=f"due_{task.id}",
                    )

                    if st.button(
                        "Save Changes",
                        key=f"save_{task.id}",
                        use_container_width=True,
                    ):
                        session = SessionLocal()

                        try:
                            db_task = session.get(
                                Task,
                                task.id,
                            )

                            if (
                                db_task
                                and db_task.user_id == user_id
                            ):
                                db_task.title = edit_title.strip()
                                db_task.description = (
                                    edit_description.strip()
                                    or None
                                )
                                db_task.priority = edit_priority
                                db_task.due_date = edit_due_date

                                session.commit()

                        finally:
                            session.close()

                        st.rerun()

            with col2:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task.id}",
                    use_container_width=True,
                ):
                    session = SessionLocal()

                    try:
                        db_task = session.get(
                            Task,
                            task.id,
                        )

                        if (
                            db_task
                            and db_task.user_id == user_id
                        ):
                            session.delete(db_task)
                            session.commit()

                    finally:
                        session.close()

                    st.rerun()


# ============================================================
# Finance
# ============================================================

def finance_page():
    st.title("💰 Finance")

    user_id = st.session_state["user_id"]
    session = SessionLocal()

    try:
        # ========================================================
        # Add Transaction
        # ========================================================

        st.subheader("Add Transaction")

        with st.form("add_transaction_form"):
            title = st.text_input(
                "Title",
                placeholder="e.g. Salary, Food, Internet",
            )

            amount = st.number_input(
                "Amount (Toman)",
                min_value=0.0,
                step=1000.0,
                format="%.0f",
            )

            transaction_type = st.selectbox(
                "Transaction Type",
                ["income", "expense"],
                format_func=lambda x: (
                    "Income" if x == "income" else "Expense"
                ),
            )

            description = st.text_area(
                "Description",
                placeholder="Optional",
            )

            submitted = st.form_submit_button(
                "Add Transaction",
                use_container_width=True,
            )

        if submitted:
            if not title.strip():
                st.error("Please enter a title.")
                return

            if amount <= 0:
                st.error("Amount must be greater than zero.")
                return

            transaction = FinancialTransaction(
                user_id=user_id,
                title=title.strip(),
                amount=Decimal(str(amount)),
                transaction_type=transaction_type,
                description=description.strip() or None,
            )

            session.add(transaction)
            session.commit()

            st.success("Transaction added successfully.")
            st.rerun()

        # ========================================================
        # Calculate Balance
        # ========================================================

        total_income = session.scalar(
            select(
                func.coalesce(
                    func.sum(FinancialTransaction.amount),
                    0,
                )
            ).where(
                FinancialTransaction.user_id == user_id,
                FinancialTransaction.transaction_type == "income",
            )
        )

        total_expense = session.scalar(
            select(
                func.coalesce(
                    func.sum(FinancialTransaction.amount),
                    0,
                )
            ).where(
                FinancialTransaction.user_id == user_id,
                FinancialTransaction.transaction_type == "expense",
            )
        )

        total_income = Decimal(str(total_income))
        total_expense = Decimal(str(total_expense))

        balance = total_income - total_expense

        # ========================================================
        # Financial Summary
        # ========================================================

        st.divider()
        st.subheader("Financial Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Income",
                f"{total_income:,.0f} Toman",
            )

        with col2:
            st.metric(
                "Total Expense",
                f"{total_expense:,.0f} Toman",
            )

        with col3:
            st.metric(
                "Current Balance",
                f"{balance:,.0f} Toman",
            )

        # ========================================================
        # Transaction History
        # ========================================================

        st.divider()
        st.subheader("Transaction History")

        transactions = session.scalars(
            select(FinancialTransaction)
            .where(
                FinancialTransaction.user_id == user_id
            )
            .order_by(
                FinancialTransaction.created_at.desc()
            )
        ).all()

        if not transactions:
            st.info("No transactions found.")
            return

        for transaction in transactions:
            if transaction.transaction_type == "income":
                icon = "🟢"
                type_label = "Income"
            else:
                icon = "🔴"
                type_label = "Expense"

            with st.container(border=True):
                col1, col2, col3 = st.columns(
                    [4, 2, 2]
                )

                with col1:
                    st.markdown(
                        f"### {icon} {transaction.title}"
                    )

                    if transaction.description:
                        st.caption(
                            transaction.description
                        )

                with col2:
                    st.write(type_label)

                with col3:
                    st.write(
                        f"{transaction.amount:,.0f} Toman"
                    )

                if st.button(
                    "Delete",
                    key=f"delete_transaction_{transaction.id}",
                ):
                    session.delete(transaction)
                    session.commit()

                    st.success(
                        "Transaction deleted."
                    )

                    st.rerun()

    finally:
        session.close()

# ============================================================
# Journal
# ============================================================

def journal_page():
    st.title("📔 Journal")
    st.caption("Write, save, and review your journal entries.")

    user_id = st.session_state["user_id"]
    session = SessionLocal()

    try:
        # ========================================================
        # Add Journal Entry
        # ========================================================

        with st.expander("➕ New Journal Entry", expanded=True):

            with st.form("journal_form"):
                title = st.text_input(
                    "Title",
                    placeholder="Optional",
                )

                entry_date = st.date_input(
                    "Date",
                    value=date.today(),
                )

                content = st.text_area(
                    "Journal Entry",
                    placeholder="Write your thoughts here...",
                    height=250,
                )

                submitted = st.form_submit_button(
                    "Save Entry",
                    use_container_width=True,
                )

            if submitted:

                if not content.strip():
                    st.error("Journal entry cannot be empty.")
                    return

                entry = JournalEntry(
                    user_id=user_id,
                    title=title.strip() or None,
                    content=content.strip(),
                    entry_date=entry_date,
                )

                session.add(entry)
                session.commit()

                st.success("Journal entry saved successfully.")
                st.rerun()

        # ========================================================
        # Monthly Calendar
        # ========================================================

        st.divider()

        st.subheader("📅 Journal Calendar")

        today = date.today()

        if "calendar_year" not in st.session_state:
            st.session_state["calendar_year"] = today.year

        if "calendar_month" not in st.session_state:
            st.session_state["calendar_month"] = today.month

        if "selected_journal_date" not in st.session_state:
            st.session_state["selected_journal_date"] = today

        current_year = st.session_state["calendar_year"]
        current_month = st.session_state["calendar_month"]

        # ========================================================
        # Get Days With Journal Entries
        # ========================================================

        month_start = date(
            current_year,
            current_month,
            1,
        )

        if current_month == 12:
            next_month = date(
                current_year + 1,
                1,
                1,
            )
        else:
            next_month = date(
                current_year,
                current_month + 1,
                1,
            )

        month_entries = session.scalars(
            select(JournalEntry)
            .where(
                JournalEntry.user_id == user_id,
                JournalEntry.entry_date >= month_start,
                JournalEntry.entry_date < next_month,
            )
        ).all()

        journal_dates = {
            entry.entry_date
            for entry in month_entries
        }

        # ========================================================
        # Month Navigation
        # ========================================================

        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            if st.button(
                    "← Previous",
                    use_container_width=True,
            ):
                if current_month == 1:
                    st.session_state["calendar_year"] -= 1
                    st.session_state["calendar_month"] = 12
                else:
                    st.session_state["calendar_month"] -= 1

                st.rerun()

        with col2:
            month_name = calendar.month_name[current_month]

            st.markdown(
                f"<h3 style='text-align:center;'>"
                f"{month_name} {current_year}"
                f"</h3>",
                unsafe_allow_html=True,
            )

        with col3:
            if st.button(
                    "Next →",
                    use_container_width=True,
            ):
                if current_month == 12:
                    st.session_state["calendar_year"] += 1
                    st.session_state["calendar_month"] = 1
                else:
                    st.session_state["calendar_month"] += 1

                st.rerun()

        # ========================================================
        # Weekday Header
        # ========================================================

        weekdays = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ]

        cols = st.columns(7)

        for index, weekday in enumerate(weekdays):
            with cols[index]:
                st.markdown(
                    f"<div style='text-align:center;"
                    f"font-weight:bold;'>{weekday}</div>",
                    unsafe_allow_html=True,
                )

        # ========================================================
        # Calendar Grid
        # ========================================================

        calendar_matrix = calendar.monthcalendar(
            current_year,
            current_month,
        )

        for week in calendar_matrix:

            cols = st.columns(7)

            for index, day in enumerate(week):

                with cols[index]:

                    if day == 0:
                        st.write("")
                        continue

                    current_date = date(
                        current_year,
                        current_month,
                        day,
                    )

                    has_entry = current_date in journal_dates



                    if has_entry:
                        label = f"{day}  ●"
                    else:
                        label = str(day)

                    if st.button(
                            label,
                            key=f"calendar_{current_year}_{current_month}_{day}",
                            use_container_width=True,
                    ):
                        st.session_state[
                            "selected_journal_date"
                        ] = current_date

                        st.rerun()

        # ========================================================
        # Selected Date
        # ========================================================

        selected_date = st.session_state[
            "selected_journal_date"
        ]

        st.divider()

        st.subheader(
            f"Journal — {selected_date.strftime('%Y-%m-%d')}"
        )

        selected_entries = session.scalars(
            select(JournalEntry)
            .where(
                JournalEntry.user_id == user_id,
                JournalEntry.entry_date == selected_date,
            )
            .order_by(
                JournalEntry.created_at.desc()
            )
        ).all()

        if not selected_entries:

            st.info(
                "No journal entries for this date."
            )

        else:

            for entry in selected_entries:

                display_title = (
                    entry.title
                    if entry.title
                    else "Untitled Entry"
                )

                with st.container(border=True):

                    st.markdown(
                        f"### 📔 {display_title}"
                    )

                    st.caption(
                        entry.entry_date.strftime(
                            "%Y-%m-%d"
                        )
                    )

                    st.write(entry.content)

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                                "Edit",
                                key=f"edit_journal_{entry.id}",
                                use_container_width=True,
                        ):
                            st.session_state[
                                f"editing_journal_{entry.id}"
                            ] = True

                    with col2:
                        if st.button(
                                "Delete",
                                key=f"delete_journal_{entry.id}",
                                use_container_width=True,
                        ):
                            session.delete(entry)
                            session.commit()
                            st.rerun()
                # ====================================================
                # Edit Entry
                # ====================================================

                if st.session_state.get(
                    f"editing_journal_{entry.id}",
                    False,
                ):

                    with st.form(
                        f"edit_journal_form_{entry.id}"
                    ):
                        edited_title = st.text_input(
                            "Title",
                            value=entry.title or "",
                        )

                        edited_date = st.date_input(
                            "Date",
                            value=entry.entry_date,
                        )

                        edited_content = st.text_area(
                            "Journal Entry",
                            value=entry.content,
                            height=250,
                        )

                        save_changes = st.form_submit_button(
                            "Save Changes",
                            use_container_width=True,
                        )

                    if save_changes:

                        if not edited_content.strip():
                            st.error(
                                "Journal entry cannot be empty."
                            )
                        else:
                            entry.title = (
                                edited_title.strip()
                                or None
                            )

                            entry.entry_date = edited_date
                            entry.content = (
                                edited_content.strip()
                            )

                            session.commit()

                            st.session_state[
                                f"editing_journal_{entry.id}"
                            ] = False

                            st.success(
                                "Journal entry updated successfully."
                            )

                            st.rerun()

    finally:
        session.close()


# ============================================================
# Settings
# ============================================================

def settings_page():
    st.title("⚙️ Settings")

    user_id = st.session_state["user_id"]

    session = SessionLocal()

    try:
        user = session.get(User, user_id)

        if user is None:
            st.error("User account not found.")
            return

        # ========================================================
        # Account
        # ========================================================

        st.subheader("Account")

        st.text_input(
            "Username",
            value=user.username,
            disabled=True,
        )

        with st.form("change_name_form"):

            full_name = st.text_input(
                "Full Name",
                value=user.full_name or "",
            )

            submitted = st.form_submit_button(
                "Change Full Name",
                use_container_width=True,
            )

            if submitted:

                if not full_name.strip():
                    st.error("Full name cannot be empty.")
                else:
                    user.full_name = full_name.strip()

                    session.commit()

                    st.session_state["full_name"] = (
                        user.full_name
                    )

                    st.success(
                        "Full name changed successfully."
                    )

        # ========================================================
        # Security
        # ========================================================

        st.divider()

        st.subheader("Security")

        with st.form("change_password_form"):

            current_password = st.text_input(
                "Current Password",
                type="password",
            )

            new_password = st.text_input(
                "New Password",
                type="password",
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
            )

            submitted = st.form_submit_button(
                "Change Password",
                use_container_width=True,
            )

            if submitted:

                if not current_password:
                    st.error(
                        "Please enter your current password."
                    )

                elif not new_password:
                    st.error(
                        "Please enter a new password."
                    )

                elif new_password != confirm_password:
                    st.error(
                        "New passwords do not match."
                    )

                elif not check_password_hash(
                    user.password_hash,
                    current_password,
                ):
                    st.error(
                        "Current password is incorrect."
                    )

                elif len(new_password) < 8:
                    st.error(
                        "New password must be at least 8 characters."
                    )

                else:
                    user.password_hash = (
                        generate_password_hash(
                            new_password
                        )
                    )

                    session.commit()

                    st.success(
                        "Password changed successfully."
                    )

        # ========================================================
        # Session
        # ========================================================

        st.divider()

        st.subheader("Session")

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
            st.session_state.clear()
            st.rerun()

    finally:
        session.close()


# ============================================================
# Main
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


if not st.session_state["logged_in"]:
    login_page()

else:
    selected_page = sidebar()

    if selected_page == "🏠 Dashboard":
        dashboard_page()

    elif selected_page == "✅ Tasks":
        tasks_page()

    elif selected_page == "💰 Finance":
        finance_page()

    elif selected_page == "📔 Journal":
        journal_page()

    elif selected_page == "⚙️ Settings":
        settings_page()

