struct = '''
create schema if not exists ton;

create table if not exists ton.wallet(
    balance numeric not null,
    wallet text not null,
    mnemonic text not null,
	primary key (mnemonic)
);

create index if not exists idx_mnemonic on ton.wallet (mnemonic);
'''