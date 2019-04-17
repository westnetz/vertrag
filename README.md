# vertrag

**vertrag** is a command line based tool to generate contract documents from yaml files.


## Features

* purely file based (no database)
* customizeable (contract layout is HTML/CSS)

## Installation

Clone this repository to your machine:

```
$ git clone https://github.com/westnetz/vertrag
```

Install the package

```
$ make install
```

**Note:** At the moment installation via pip only works, if you provide the -e option. Therefore it is recommended to use the provided *make install* method.

## Getting Started

This section is a quick walkthrough all the features.

### Initialization

Before you can start generating your own contracts you need to setup your working directory for *vertrag*. By invoking

```
$ vertrag init
```

all required directory and configuration files will be placed in the current working directory. It is recommended to do this in a clean directory or in your already
existing or to-be-working-directory for [rechnung](https://github.com/westnetz/rechnung)

### Configuration and Customization

You can now edit the *vertrag.config.yaml* file to your needs. You need to enter the credentials for the mail server if you want to send out your contracts by email.

Customization of the invoices can be done by editing the invoice template *templates/contract_template.j2.html* and the corresponding stylesheet in *assets/contract.css*. 

### Contract Creation

You copy your request-yaml-files originating e.g. from [anschluss](https://github.com/westnetz/anschluss) to your *anschluss* directory. 
The following command

```
$ vertrag create ANSCHLUSS_REQUEST_ID 
```

will create the contract yaml. Some information has to be entered by you e.g. the monthly price.

### PDF Creation

If everything is correct, you are ready to create your pdf contracts.

```
$ vertrag render CONTRACT_ID
```

This command will render your contract. 

### Contract Delivery

If you want to use the included mail delivery service, you should customize the invoice mail template to your needs: *templates/contract_mail_template.j2*. 

After doing that, you can send the contract to your customer:

```
$ vertrag send CONTRACT_ID
```

And that's it!

## Copyright

F. Rämisch, 2019

## License

GNU General Public License v3
