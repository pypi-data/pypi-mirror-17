# Change Log

## 4.0.2

### Fixed

 - More understandable names for the exceptions.
 - Refactor retries in client
 - Add test for timeouts. TODO: add test for retries.

## 4.0.1

### Added

 - LBSM load balancer

## 4.0.0

### Added

 - New API for client builders.
 - Client builders for LB, Session and NCBI clients.

## 3.1.5

### Fixed

 - Check if passed session was modified by ahoyhoy and do NOT do it again if it was.


## 3.0.0 - 08/08/2016

### Added

 - Circuit breaker
 - Load balancers
 - Retries
 - Docs
 - First pass at separating NCBI stuff

## 2.0.0 - 05/26/2016

### Added

 - Introduce NCBISession object for passing NCBI-SID and NCBI-PHID headers.
 - DTAB extraxtion from Django request.


## 1.0.0 - 04/20/2016

### Added

- Initial implementation
- All the requests methods are implemented to support PhID
- Simple LBOS resolver
