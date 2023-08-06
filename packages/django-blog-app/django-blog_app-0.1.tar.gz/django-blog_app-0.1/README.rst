=====
Blog
=====

Blog is a Django blog app 
Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "blog" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = [
               ...
                       'blog',
                           ]

                        2. Include the polls URLconf in your project urls.py like this::

                        url(r'^', include('blog.urls', namespace='blog', app_name='blog')),
                            
                            3. Run `python manage.py migrate` to create the polls models.

                            4. Start the development server and visit http://127.0.0.1:8000/admin/
                                  to create blog posts (you'll need the Admin app enabled).

