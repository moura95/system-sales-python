create type public.originleadsenum as enum ('Facebook', 'Instagram', 'Whatsapp', 'Google', 'Linkedin', 'Outros');

create type public.plantype as enum ('Free', 'Silver', 'Gold');

create type public.companytypeenum as enum ('Cliente', 'Transportadora', 'Fabrica');

create type public.shippingenum as enum ('Entrega', 'Retirada', 'Outros');

create type public.statusenum as enum ('Pendente', 'Aprovado', 'Cancelada');

create type public.paymenttypeenum as enum ('Pagamento', 'Recebimento');

create type public.paymentreceiptstatusenum as enum ('Pendente', 'Pago', 'Cancelado');


create table if not exists public.alembic_version
(
    version_num varchar(32) not null
        constraint alembic_version_pkc
            primary key
);


create table if not exists public.core_leads
(
    id         serial
        primary key,
    name       varchar                 not null,
    email      varchar                 not null,
    phone      varchar                 not null,
    origin     originleadsenum         not null,
    is_active  boolean                 not null,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null
);


create table if not exists public.core_tenants
(
    id           serial
        primary key,
    cpf_cnpj     varchar(11),
    name         varchar(50),
    fantasy_name varchar(50),
    ie           varchar(20),
    phone        varchar(20),
    email        varchar(100),
    website      varchar(100),
    logo_url     varchar(100),
    plan         plantype,
    stripe_id    varchar(100),
    data_expire  timestamp,
    is_active    boolean                 not null,
    created_at   timestamp default now() not null,
    updated_at   timestamp default now()
);

create table if not exists public.core_address
(
    id         serial
        primary key,
    type       varchar(11)             not null,
    zip_code   varchar(50),
    street     varchar(50),
    number     varchar(50),
    district   varchar(50),
    complement varchar(50),
    state      varchar(50)             not null,
    city       varchar(50)             not null,
    tenant_id  integer                 not null
        references public.core_tenants
            on delete cascade,
    is_active  boolean                 not null,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null
);


create table if not exists public.core_companies
(
    id                serial
        primary key,
    tenant_id         integer                 not null
        references public.core_tenants
            on delete cascade,
    company_type      companytypeenum         not null,
    name              varchar(50),
    last_fantasy_name varchar(50),
    cpf_cnpj          varchar(11),
    rg_ie             varchar(20),
    phone             varchar(20),
    email             varchar(100),
    is_active         boolean                 not null,
    created_at        timestamp default now() not null,
    updated_at        timestamp default now() not null
);


create table if not exists public.core_customizations
(
    id          serial
        primary key,
    tenant_id   integer                 not null
        references public.core_tenants
            on delete cascade,
    key         varchar                 not null,
    value       varchar                 not null,
    title       varchar                 not null,
    type        varchar                 not null,
    changleable boolean                 not null,
    created_at  timestamp default now() not null,
    updated_at  timestamp default now()
);


create table if not exists public.core_files
(
    id         serial
        primary key,
    tenant_id  integer                 not null
        references public.core_tenants
            on delete cascade,
    name       varchar                 not null,
    dir        varchar                 not null,
    url_file   varchar                 not null,
    created_at timestamp default now() not null
);


create table if not exists public.core_form_payments
(
    id        serial
        primary key,
    tenant_id integer not null
        references public.core_tenants
            on delete cascade,
    name      varchar not null
);


create table if not exists public.core_sellers
(
    id          serial
        primary key,
    tenant_id   integer                 not null
        references public.core_tenants
            on delete cascade,
    cpf         varchar(11)             not null,
    name        varchar(50)             not null,
    phone       varchar(20),
    email       varchar(100),
    pix         varchar(100),
    observation varchar(100),
    is_active   boolean                 not null,
    created_at  timestamp default now() not null,
    updated_at  timestamp default now() not null
);



create table if not exists public.core_services
(
    id          serial
        primary key,
    tenant_id   integer                 not null
        references public.core_tenants
            on delete cascade,
    name        varchar(255)            not null,
    code        varchar(255),
    description varchar(255),
    price       double precision        not null,
    file_url    varchar,
    is_active   boolean,
    created_at  timestamp default now() not null,
    updated_at  timestamp default now() not null
);


create table if not exists public.core_smtp
(
    id         serial
        primary key,
    tenant_id  integer                 not null
        references public.core_tenants
            on delete cascade,
    is_active  boolean                 not null,
    email      varchar                 not null,
    password   varchar                 not null,
    server     varchar(100)            not null,
    port       integer                 not null,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null
);



create table if not exists public.core_users
(
    id         serial
        primary key,
    tenant_id  integer                 not null
        references public.core_tenants
            on delete cascade,
    email      varchar                 not null
        unique,
    password   varchar                 not null,
    first_name varchar(50),
    last_name  varchar(50),
    is_active  boolean,
    last_login timestamp               not null,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null
);


create table if not exists public.core_activity
(
    id            serial
        primary key,
    action        varchar(20)             not null,
    reference_url varchar                 not null,
    user_id       integer                 not null
        references public.core_users
            on delete cascade,
    tenant_id     integer                 not null
        references public.core_tenants
            on delete cascade,
    created_at    timestamp default now() not null,
    updated_at    timestamp default now() not null
);


create table if not exists public.core_calendars
(
    id          serial
        primary key,
    title       varchar                 not null,
    visit_start timestamp,
    visit_end   timestamp,
    all_day     boolean,
    user_id     integer                 not null
        references public.core_users
            on delete cascade,
    created_at  timestamp default now() not null,
    updated_at  timestamp default now() not null
);


create table if not exists public.core_companies_address
(
    address_id integer
        references public.core_address,
    company_id integer
        references public.core_companies
);



create table if not exists public.core_orders
(
    id              serial
        primary key,
    tenant_id       integer                 not null
        references public.core_tenants
            on delete cascade,
    customer_id     integer                 not null
        references public.core_companies,
    portage_id      integer
        references public.core_companies,
    seller_id       integer                 not null
        references public.core_users,
    form_payment_id integer                 not null
        references public.core_form_payments,
    order_number    varchar(50)             not null,
    url_pdf         varchar(100),
    buyer           varchar(50),
    shipping        shippingenum            not null,
    status          statusenum              not null,
    created_at      timestamp default now() not null,
    updated_at      timestamp default now() not null,
    expired_at      timestamp default now() + interval '30 days',
    contact_date    timestamp,
    delivery_date   timestamp,
    total           double precision,
    total_products  double precision,
    total_services  double precision,
    is_active       boolean                 not null
);


create table if not exists public.core_payments_receipts
(
    id                   serial
        primary key,
    tenant_id            integer                  not null
        references public.core_tenants
            on delete cascade,
    type_payment         paymenttypeenum          not null,
    status               paymentreceiptstatusenum not null,
    description          varchar(150)             not null,
    amount               double precision         not null,
    expiration_date      timestamp,
    payment_date         timestamp,
    doc_number           varchar(50),
    recipient            varchar(50),
    form_payment         integer                  not null
        references public.core_form_payments
            on update cascade,
    is_active            boolean                  not null,
    installment          integer                  not null,
    numbers_installments integer                  not null,
    interval_days        integer                  not null,
    additional_info      varchar(50)              not null,
    created_at           timestamp default now()  not null,
    updated_at           timestamp default now()  not null
);


create table if not exists public.core_products
(
    id            serial
        primary key,
    tenant_id     integer                 not null
        references public.core_tenants
            on delete cascade,
    factory_id    integer
        references public.core_companies
            on delete cascade,
    name          varchar(255)            not null,
    code          varchar(255),
    bar_code      varchar(255),
    price         double precision        not null,
    cost_value    double precision,
    reference     varchar,
    unit          varchar,
    description   varchar,
    image_url     varchar,
    minimum_stock integer,
    maximum_stock integer,
    current_stock integer                 not null,
    active_pdv    boolean                 not null,
    is_active     boolean                 not null,
    created_at    timestamp default now() not null,
    updated_at    timestamp default now() not null
);

create table if not exists public.core_sellers_address
(
    address_id integer
        references public.core_address,
    seller_id  integer
        references public.core_sellers
);


create table if not exists public.core_tenants_address
(
    address_id integer
        references public.core_address,
    tenant_id  integer
        references public.core_tenants
);


create table if not exists public.core_users_address
(
    address_id integer
        references public.core_address,
    user_id    integer
        references public.core_users
);


create table if not exists public.core_orders_files
(
    order_id integer
        references public.core_orders
            on delete cascade,
    file_id  integer
        references public.core_files
            on delete cascade
);


create table if not exists public.core_orders_product
(
    order_id   integer
        references public.core_orders,
    product_id integer
        references public.core_products,
    quantity   integer,
    price      double precision,
    discount   double precision,
    total      double precision
);


create table if not exists public.core_payments_files
(
    payment_id integer
        references public.core_payments_receipts
            on delete cascade,
    file_id    integer
        references public.core_files
            on delete cascade
);


create table if not exists public.core_orders_services
(
    order_id   integer
        references public.core_orders,
    service_id integer
        references public.core_services,
    price      double precision,
    discount   double precision,
    quantity   integer,
    total      double precision
);


CREATE TABLE if not exists public.core_history_stock
(
    id           SERIAL PRIMARY KEY,
    product_id   INTEGER REFERENCES core_products (id) ON DELETE CASCADE,
    tenant_id    INTEGER REFERENCES core_tenants (id) ON DELETE CASCADE,
    user_id      INTEGER REFERENCES core_users (id) ON DELETE CASCADE,
    reason       VARCHAR,
    before_stock INTEGER,
    after_stock  INTEGER,
    observation  VARCHAR,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);