INSERT INTO public.core_tenants (cnpj, name, fantasy_name, ie, phone,
                                 email, website, logo_url, plan, stripe_id,
                                 data_expire, is_active, created_at,
                                 updated_at)
VALUES (null, null, null, null, null, null, null, null, 'Free', null,
        '2023-08-17 20:26:14.551946', true, '2023-07-18 23:26:14.552930',
        '2023-07-18 23:26:14.552930');


INSERT INTO public.core_users (tenant_id, email, password, first_name,
                               last_name, is_active, last_login, created_at,
                               updated_at)
VALUES (1, 'jr@hotmail.com',
        '$2b$12$eOwSVbfkUH8YzQvSk9zPiOlNWkh6z7WbVCj2jIQl29uoOFo6ZxDoG',
        'string', 'string', true, '2023-07-18 23:00:06.755556',
        '2023-07-18 23:00:06.755556', '2023-07-18 23:00:06.755556');


INSERT INTO public.core_form_payments (tenant_id, name)
VALUES (1, '30/45/60');


INSERT INTO public.core_companies (tenant_id, company_type, is_individual,
                                   cpf_cnpj,
                                   name, last_fantasy_name, rg_ie, phone,
                                   email, is_active,
                                   created_at, updated_at)
VALUES (1, 'Cliente', true, 'string', 'string', null, 'string', 'string',
        'string',
        true, '2023-07-18 23:00:28.352391', '2023-07-18 23:00:28.352391');

INSERT INTO public.core_companies (tenant_id, company_type, is_individual,
                                   cpf_cnpj,
                                   name, last_fantasy_name, rg_ie, phone,
                                   email, is_active,
                                   created_at, updated_at)
VALUES (1, 'Transportadora', false, 'string', 'string', null, 'string',
        'string',
        'string',
        true, '2023-07-18 23:00:28.352391', '2023-07-18 23:00:28.352391');

INSERT INTO public.core_companies (tenant_id, company_type, is_individual,
                                   cpf_cnpj,
                                   name, last_fantasy_name, rg_ie, phone,
                                   email, is_active,
                                   created_at, updated_at)
VALUES (1, 'Fornecedor', false, 'string', 'string', null, 'string', 'string',
        'string',
        true, '2023-07-18 23:00:28.352391', '2023-07-18 23:00:28.352391');

INSERT INTO public.core_sellers (tenant_id, cpf, name, phone, email, pix,
                                 observation, is_active, created_at,
                                 updated_at)
VALUES (1, '55454', 'test', null, null, null, null, true,
        '2023-07-18 23:23:52.168111', '2023-07-18 23:23:52.168111');

INSERT INTO public.core_orders (tenant_id, customer_id, portage_id,
                                seller_id, form_payment_id, order_number,
                                url_pdf,
                                buyer, shipping, status, created_at,
                                expired_at,
                                contact_date, delivery_date, total,
                                is_active)
VALUES (1, 1, 2, 1, 1, 'string', 'string', 'string', 'Entrega', 'Pendente',
        '2023-08-18 23:03:08.230903', '2023-08-18 23:03:08.230903', null, null,
        null, true);

INSERT INTO public.core_products (tenant_id, factory_id, name, code, bar_code,
                                  price, cost_value, reference, unit,
                                  description, image_url, minimum_stock,
                                  maximum_stock, current_stock, active_pdv,
                                  is_active, created_at, updated_at)
VALUES (1, null, '<string>', '<string>', '<string>', 10.9, 5, '<string>',
        '<string>', '<string>', '<string>', 0, 0, 100, true, true,
        '2023-07-17 15:16:53.123309', '2023-07-17 15:16:53.123309');
INSERT INTO public.core_products (tenant_id, factory_id, name, code, bar_code,
                                  price, cost_value, reference, unit,
                                  description, image_url, minimum_stock,
                                  maximum_stock, current_stock, active_pdv,
                                  is_active, created_at, updated_at)
VALUES (1, null, '<string>', '<string>', '<string>', 10.9, 5, '<string>',
        '<string>', '<string>', '<string>', 0, 0, 100, true, true,
        '2023-07-17 18:35:29.420514', '2023-07-17 18:35:29.420514');
INSERT INTO public.core_services (id, tenant_id, name, code, description, price, file_url, is_active, created_at, updated_at) VALUES (1, 1, 'eletrica do banheiro', 'e123', 'passagem de cabo e instalacao', 1000, null, true, '2023-09-22 19:07:51.405114', '2023-09-22 19:07:51.405114');
INSERT INTO public.core_services (id, tenant_id, name, code, description, price, file_url, is_active, created_at, updated_at) VALUES (2, 1, 'carpintaria', 'e321', 'pintura', 500, null, true, '2023-09-22 19:07:51.405114', '2023-09-22 19:07:51.405114');



INSERT INTO public.core_customizations(tenant_id, key, value, title, type,
                                       changeable)
values (1, 'GENERIC_TYPE', 'GENERIC_VALUE', 'GENERIC_TITLE', 'STRING', true);

INSERT INTO public.core_orders_products (order_id, product_id, quantity, price, discount, total) VALUES (1, 1, 10, 100, 0, 1000);
INSERT INTO public.core_orders_products (order_id, product_id, quantity, price, discount, total) VALUES (1, 2, 1, 200, 0, 200);

INSERT INTO public.core_orders_services (order_id, service_id, quantity, price, discount, total) VALUES (1, 1, 10, 100, 0, 1000);
INSERT INTO public.core_orders_services (order_id, service_id, quantity, price, discount, total) VALUES (1, 2, 1, 200, 0, 200);

