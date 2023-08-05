from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), "lino_shop",
    # tolerate_sphinx_warnings=True,
    locale_dir='lino_shop/lib/shop/locale',
    revision_control_system='git',
    cleanable_files=['docs/api/lino_shop.*'],
    demo_projects=['lino_shop.projects.shop1'])
